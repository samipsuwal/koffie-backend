from distutils.log import ERROR
import json
from msilib.schema import Error
from unittest import result
from pydantic import Json
import schema
import httpx
import re

#should come from a settings file or equivalent
CLIENT_URL ="https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{}?format={}"

VIN_PATTERN = re.compile(r'[a-zA-Z0-9]{17}')

#ENd of settings

#function to extract vehicle from the VEHICLE API response
def get_entity_from_response(response):
    try:
        #aren't VINs unique??  
        return response["Results"][0]
    except Exception as ex:
        return ex

#Construct URL for request
def construct_url_using_vin(vin):
    try:
        return CLIENT_URL.format(vin,"JSON")
    except Exception as ex:
        return ex

#using the schema 
def parse_vehicle(vehicle_to_be_parsed):
    try:
        return schema.Vehicle(**vehicle_to_be_parsed)
    except Exception as ex:
        return ex

#calls the client service API for the vehicle using VIN
async def get_vehicle_from_client(vin):
    try:
        url_for_request = construct_url_using_vin(vin)
        #send request to the client
        async with httpx.AsyncClient() as client:
            response = await client.get(url_for_request)
        
        vehicle_from_response = get_entity_from_response(response.json())
        
        #call the parser to filter attributes that we need 
        return parse_vehicle(vehicle_from_response)
    except Exception as ex:
        return ex

#using re library does a match of vin against VIN_PATTERN
def validate_vin(vin):
    try:
        if re.fullmatch(VIN_PATTERN, vin):
            return True
        return False
    except Exception as ex:
        return ex
    


from pyspark.sql import SparkSession, Row
spark = SparkSession.builder.getOrCreate()
from pyspark.sql.types import StructType, StructField, StringType

def convert_json_to_par(json_data):
    return "Success"


