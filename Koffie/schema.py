from pydantic import BaseModel
from typing import Optional

#models/data/validation
class Vehicle(BaseModel):
    VIN:str
    Make:str
    Model:str
    ModelYear:str
    BodyClass:str
    CachedResult: Optional[bool] = False