import models
import schemas
from fastapi import HTTPException


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_username(username: str):
    return models.User.filter(models.User.username == username).first()


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    user = models.User(
        username=user.username,
        password=fake_hashed_password,
        phone=user.phone,
        email=user.email
    )
    user.save()
    return user


def get_ride(ride_id: int):
    ride = models.Ride.filter(models.Ride.id == ride_id).first()
    ride.__data__['passenger_ids'] = get_confirmed_passengers_by_ride(ride_id)
    return ride.__data__


def create_ride(ride: schemas.RideCreate):
    ride = models.Ride(**ride.dict())
    ride.save()
    return ride.__data__


def reserve_ride(ride_id: int):
    ride = get_ride(ride_id)
    models.RidePassenger.create(
        ride=ride_id,
        passenger=models.User.filter(models.User.id == 4).first().id
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
