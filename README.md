# vehicle-api-backend
backend-assessment for [Koffie Labs](https://getkoffie.com/) 

APIS build on [FastAPI](https://fastapi.tiangolo.com/). Returns Vehicle information according to VIN. Backed by [vPIC API](https://vpic.nhtsa.dot.gov/api/), and uses [SQLite](https://www.sqlite.org/index.html) for cache.

---
### 1- Look_Up
Grab vehicle information according to the VIN. If available get from SQLite Cache.

Otherwise, grab from vPIC API and update Cache accordingly

URL: `/lookup/{VIN}`

Example: `/lookup/1XPWD40X1ED215307`

Method: `GET`

Params: 

    - VIN
    Type: String 
    Validation: 17 alphanumeric characters  


Returns: 

  Type: JSON
  
    {
      VIN: String
      Make: String
      Model: String
      ModelYear: String
      BodyClass: String
    }
  
 ---
  
### 2- Remove
URL: `/remove/{VIN}`

Example: `/remove/1XPWD40X1ED215307`

Method: `GET`

Params: 

    - VIN
    Type: String 
    Validation: 17 alphanumeric characters  


Returns: 

  Type: JSON
  
    {
      VIN: String
      cached_delete: Boolean
    }
  
 ---
 
 ### 3- Export
URL: `/export`

Example: `/export`

Method: `GET`

Params: 

    N/A

Returns: 

  Type: Paraquet file
  
  
 ---
 
