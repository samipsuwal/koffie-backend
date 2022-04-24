from http.client import HTTPException
from databases import Database
from fastapi import FastAPI
import services

database = Database("sqlite:///test.db")

app = FastAPI()

@app.on_event("startup")
async def database_connect():
    await database.connect()

@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


#Database layer
#subject to sql injection
async def get_cached_vehicle_by_VIN(vin):
    try:
        query="SELECT * FROM VEHICLES WHERE VIN='{}';".format(vin)
        vehicle_from_database = await database.fetch_one(query= query)
        #vehicle_from_database["CachedResult"] = True #do we want to save this in database? 
        return vehicle_from_database
    except Exception as ex:
        return ex


async def insert_vehicle_into_database(vehicle):
    try:
        query="INSERT into VEHICLES (VIN, MAKE, MODEL, MODELYEAR, BODYCLASS)  VALUES ( '" + vehicle.VIN +"', '"+ vehicle.Make+"', '" + vehicle.Model+"', '" + vehicle.ModelYear+"', '" + vehicle.BodyClass + "');"
        result = await database.execute(query= query)
        return result
    except Exception as ex:
        return ex

async def remove_vehicle_from_database(vin):
    try:
        query="DELETE FROM VEHICLES WHERE VIN ='{}';".format(vin)
        await database.execute(query=query)
    except Exception as ex:
        return ex

async def get_all_vehicles_from_database():
    try:
        query = "SELECT VIN FROM VEHICLES"
        result = await database.fetch_all(query=query)
        return result
    except Exception as ex:
        return ex

##END of Database Layer
    

#Beginning of routes

#API that returns VIN either from Cache or Client
#params-VIN
#return JSON response
@app.get("/lookup/{vin}")
async def lookup(vin: str):
    try:
        #TODO make sure the VIN is valid 17 alpha numeric
        if services.validate_vin(vin) is False:
            raise HTTPException(status_code=404, detail="Not Found")
            #return "Invalid VIN {}".format(vin)


        #get the vehicle from the database, service layer -> database layer
        cached_vehicle = await get_cached_vehicle_by_VIN(vin)

        if cached_vehicle is not None:
            #parsed_vehicle = services.parse_vehicle(cached_vehicle)
            vehicle_to_return = cached_vehicle
            #vehicle_to_return["CachedResult"] = True
            return vehicle_to_return
        
        #vic wasn't found in the database or forced key was used
        requested_vehicle_from_client = await services.get_vehicle_from_client(vin)

        #the service should call database layer. 
        ##this doesn't has to be a blocking call, we can send the request back to the user, while asynchronously updating the database
        await insert_vehicle_into_database(requested_vehicle_from_client)
        
        return requested_vehicle_from_client
    except:
        raise HTTPException(status_code=500, detail="Server Error")



#API that removes entry from the Cache
#params: vin
#return success we are not going to send more specific message for security
@app.get("/remove/{vin}")
async def remove(vin: str):
    try:
        if services.validate_vin(vin) is False:
            return "Invalid VIN {}".format(vin)

        await remove_vehicle_from_database(vin)
        return "Success"
    except:
        raise HTTPException(status_code=500, detail="Server Error")


#Export the SQLLite cache in Parquet format
@app.get("/export")
async def export():
    try:
        all_vehicles = await get_all_vehicles_from_database() 
        data_parquet_format = services.convert_json_to_par(all_vehicles)

        return data_parquet_format
    except:
        raise HTTPException(status_code=500, detail="Server Error")


#End of routes