import os

from uuid import uuid4
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')

app = FastAPI(
    title='Car API',
    description='Car API with FastAPI and MongoDB',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class Car(BaseModel):
    brand: str
    model: str

    color: str
    description: str

    year: int
    type: str

    image: str
    price: int

    available: bool = True


client = MongoClient(MONGO_URL)
db = client['car']['production']


def find_car(car_id: str):
    document = db.find_one({'_id': car_id})

    if not document:
        raise HTTPException(status_code=404, detail=f'car \'{car_id}\' not found')

    return document


# car crud

@app.post(
    '/car',
    description='Create a new car entry.',
    response_description='Confirmation message with the created car ID.'
)
async def create_car(car: Car):
    car_id = str(uuid4())

    db.insert_one({'_id': car_id, **car.model_dump()})

    return {'message': f'created: {car_id}', 'id': car_id}


@app.get(
    '/car/{car_id}',
    description='Retrieve details of a specific car by its ID.',
    response_description='Details of the car if found, or 404 if the car was not found.'
)
async def read_car(car_id: str):
    return find_car(car_id)


@app.put(
    '/car/{car_id}',
    description='Update details of a specific car by its ID.',
    response_description='Confirmation message with the updated car ID.'
)
async def update_car(car_id: str, car: Car):
    find_car(car_id)

    db.update_one({'_id': car_id}, {'$set': car.model_dump()})

    return {'message': f'updated: {car_id}'}


@app.delete(
    '/car/{car_id}',
    description='Delete a car entry by its ID.',
    response_description='Confirmation message with the deleted car ID.'
)
async def delete_car(car_id: str):
    find_car(car_id)

    db.delete_one({'_id': car_id})

    return {'message': f'deleted: {car_id}'}


# cars search


@app.get(
    '/cars/',
    description='Retrieve details of all cars.',
    response_description='List of cars (empty if there are none).'
)
async def read_cars():
    return list(db.find())
