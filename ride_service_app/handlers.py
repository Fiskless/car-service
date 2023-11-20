from fastapi import Depends, HTTPException
import crud
import schemas
from router import router
from database import get_db


@router.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    '''
    Эндпоинт для создания пользователей
    '''

    db_user = crud.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(user=user)


@router.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    '''
    Эндпоинт для получения пользователя по id
    '''
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/rides/", response_model=schemas.RideCreate, dependencies=[Depends(get_db)])
def create_ride(ride: schemas.RideCreate):
    '''
    Эндпоинт для создания поездки
    '''
    return crud.create_ride(ride)


@router.get(
    "/rides/{ride_id}", response_model=schemas.Ride, dependencies=[Depends(get_db)]
)
def read_ride(ride_id: int):
    '''
    Эндпоинт для получения поездки по id
    '''
    db_ride = crud.get_ride(ride_id=ride_id)
    if db_ride is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return db_ride


@router.post("/reserve_ride/{ride_id}", response_model=schemas.Ride, dependencies=[Depends(get_db)])
def reserve_ride(ride_id: int):
    '''
    Эндпоинт для бронирования поездки пользователем
    '''
    return crud.reserve_ride(ride_id)


@router.post("/confirm_reserve_ride/{ride_id}/{passenger_id}", response_model=schemas.Ride, dependencies=[Depends(get_db)])
def confirm_reserve_ride(ride_id: int, passenger_id: int):
    '''
    Эндпоинт подтверждения бронирования поездки водителем
    '''
    return crud.confirm_ride(ride_id, passenger_id)
