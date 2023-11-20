from datetime import datetime

from pydantic import BaseModel, Field


class RideBase(BaseModel):
    price: int
    start_location: str
    end_location: str
    start_at: datetime
    end_at: datetime

    class Config:
        orm_mode = True


class RideCreate(RideBase):
    pass


class RideOut(RideBase):
    driver_id: int


class Ride(RideBase):
    id: int
    driver_id: int
    passenger_ids: list = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = Field(..., min_length=1)
    email: str = Field(None, min_length=1)
    phone: str = Field(..., min_length=1)

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=1)


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    token: str