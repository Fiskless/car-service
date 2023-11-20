from fastapi import FastAPI
import database
import models
from handlers import router


database.db.connect()
database.db.create_tables([models.User, models.Ride, models.RidePassenger])
database.db.close()


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = get_application()

sleep_time = 10
