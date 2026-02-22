from fastapi import FastAPI
import uvicorn
from fetch_data import fetch_data, pollution_check
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Air Quality Tracker API"}

@app.get("/health")
def health_check():
    return {"message": "API is healthy"}


@app.get("/weather/{city}")
def get_weather(city: str):
    return json.loads(fetch_data(city))

@app.get("/pollution/{city}")
def get_pollution(city: str):
    return json.loads(pollution_check(city))

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
