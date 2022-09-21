import os
from deta import Deta
from dotenv import load_dotenv

# load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)
db = deta.Base("rainfall_records")

def insert_rainfall(date, rainfall, observation):
    return db.put({"key": date, "rainfall": rainfall, "observation": observation})

def fetch_all_dates():
    res = db.fetch()
    return res.items

def get_month(month):
    return db.get(month)

