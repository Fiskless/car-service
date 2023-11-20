import peewee

from database import db


class User(peewee.Model):
    username = peewee.CharField(verbose_name='Имя', unique=True)
    password = peewee.CharField(verbose_name='Фамилия')
    email = peewee.CharField(verbose_name='Почта', null=True)
    phone = peewee.CharField(verbose_name='Телефон')

    class Meta:
        database = db


class Ride(peewee.Model):
    STATUS = [
        (1, 'Ожидание'),
        (2, 'Выполнена'),
    ]

    driver_id = peewee.ForeignKeyField(User, backref='driver_rides')

    price = peewee.CharField(verbose_name='Цена')
    start_location = peewee.CharField(verbose_name='Начальное местоположение', index=True)
    end_location = peewee.CharField(verbose_name='Конечное местоположение', index=True)
    start_at = peewee.CharField(verbose_name='Время начала поездки', index=True)
    end_at = peewee.CharField(verbose_name='Время окончания поездки', index=True)
    status = peewee.CharField(
        verbose_name='Статус',
        choices=STATUS,
        default=1
    )
    #TODO добавить валидацию

    class Meta:
        database = db


class RidePassenger(peewee.Model):
    ride = peewee.ForeignKeyField(Ride, backref='passengers')
    passenger = peewee.ForeignKeyField(User, backref='rides')
    is_confirmed = peewee.BooleanField(default=False)

    class Meta:
        database = db
        indexes = (
            (('ride', 'passenger'), True),
        )

