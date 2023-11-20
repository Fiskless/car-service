import models
import schemas
from fastapi import Depends, HTTPException
import secrets
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_username(username: str):
    return models.User.filter(models.User.username == username).first()


def get_user_by_token(token: str):
    return models.User.filter(models.User.token == token).first()


def create_user(user: schemas.UserCreate, pwd_context):
    pwd_hash = pwd_context.hash(user.password)
    token = secrets.token_hex(32)
    user = models.User(
        username=user.username,
        password=pwd_hash,
        phone=user.phone,
        email=user.email,
        token=token
    )
    user.save()
    return user


def get_ride(ride_id: int):
    ride = models.Ride.filter(models.Ride.id == ride_id).first()
    ride.__data__['passenger_ids'] = get_confirmed_passengers_by_ride(ride_id)
    return ride.__data__


def create_ride(ride: schemas.RideCreate, user):
    user_id = user.id
    ride = models.Ride(**ride.dict(), driver_id=user_id)
    ride.save()
    return ride.__data__


def reserve_ride(ride_id: int, user):
    ride = get_ride(ride_id)
    user_id = user.id
    models.RidePassenger.create(
        ride=ride_id,
        passenger=models.User.filter(models.User.id == user_id).first().id
    )
    ride['passenger_ids'] = get_confirmed_passengers_by_ride(ride_id)
    return ride


def get_confirmed_passengers_by_ride(ride_id: int):
    query = (models.RidePassenger
             .select()
             .join(models.Ride)
             .where((models.Ride.id == ride_id) & (models.RidePassenger.is_confirmed == True)))
    return [passenger.passenger.id for passenger in query]


def raise_error(field, msg):
    if field is None:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )


def confirm_ride(ride_id: int, passenger_id: int):
    ride = get_ride(ride_id)
    raise_error(ride, f"Ride with id={ride_id} does not exist")

    passenger = get_user(passenger_id)
    raise_error(passenger, f"Passenger with id={passenger_id} does not exist")

    ride_passenger = models.RidePassenger.filter(
        (models.RidePassenger.passenger == passenger_id) &
        (models.RidePassenger.ride == ride_id)
    ).first()
    raise_error(ride_passenger, f"Passenger with id={passenger_id} does not exist in ride with id={ride_id}")
    ride_passenger.is_confirmed = True
    ride_passenger.save()

    ride['passenger_ids'] = get_confirmed_passengers_by_ride(ride_id)
    return ride


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = get_user_by_token(token=token)
    if not user:
        raise HTTPException(status_code=401, detail="Неправильный токен")
    return user
