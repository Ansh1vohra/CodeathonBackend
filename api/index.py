from fastapi import FastAPI
from pydantic import BaseModel
# import joblib 
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

MONGODB_URI="mongodb+srv://anshvohra1:mongoDB.password01@cluster0.m6bujl9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = AsyncIOMotorClient(MONGODB_URI)
db = client.codeathon
users_collection = db.Users

# model = joblib.load("model.pkl")

origins = [
    "http://localhost:3000",  # React app
    "https://your-production-domain.com"  # Add your production domain here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    time: str
    machine: str
    component: str
    parameter: str
    value: float

@app.get("/")
def Home():
    return {"message": "Server Team 92 208C Code-a-Thon."}

# @app.post("/process")
# def process_data(data: RequestData):
#     input_data = [[data.time, data.machine, data.component, data.parameter, data.value]]
    
#     prediction = model.predict(input_data)
#     return {
#         # "time": data.time,
#         # "machine": data.machine,
#         # "component": data.component,
#         # "parameter": data.parameter,
#         # "value": data.value,
#         "prediction": prediction.tolist() 
#     }

class User(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: User):
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)

    return {"id": str(result.inserted_id), "message": "User created successfully"}