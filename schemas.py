from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type : str    
    
class AddressBase(BaseModel):
    name:str
    latitude:float
    longitude:float

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id:int

    class Config:
        orm_mode = True