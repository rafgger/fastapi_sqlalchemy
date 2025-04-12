from app import models, note
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from .database import engine, get_db, SessionLocal
# from dotenv import load_dotenv # removed for Docker
import os
import requests
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
# from .note import get_coin_id


models.Base.metadata.create_all(bind=engine)
# load_dotenv() # removed for Docker

app = FastAPI()
scheduler = BackgroundScheduler()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(note.router, tags=['Notes'], prefix='/api/notes')


def get_coin_id(symbol_or_name):
    """
    Retrieve the CoinGecko coin ID for a given symbol or name.
    """
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        symbol_or_name = symbol_or_name.lower()
        for coin in coins:
            if coin['symbol'].lower() == symbol_or_name or coin['name'].lower() == symbol_or_name:
                return coin['id']
        raise HTTPException(status_code=404, detail="Coin not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch coin list from CoinGecko")



def update_all_note_prices():
    db: Session = SessionLocal()
    try:
        notes = db.query(models.Note).all()
        api_key = os.getenv("API_KEY")
        if not api_key:
            print("API key not configured")
            return

        for note in notes:
            coin_id = get_coin_id(note.title)
            if not coin_id:
                print(f"Coin ID not found for {note.title}")
                continue

            url = (
                f"https://api.coingecko.com/api/v3/simple/price"
                f"?ids={coin_id}"
                f"&vs_currencies=usd"
                f"&x_cg_demo_api_key={api_key}"
            )

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                price = data.get(coin_id, {}).get("usd")
                if price is not None:
                    note.content = f"Current {note.title} price (USD):\n${price}"
                    db.add(note)
            else:
                print(f"Failed to fetch price for {note.title}: {response.status_code}")

        db.commit()
        print("All note prices updated successfully.")
    except Exception as e:
        print(f"Error updating note prices: {e}")
    finally:
        db.close()

# Schedule the job to run every 30 minutes
scheduler.add_job(update_all_note_prices, "interval", minutes=1)
scheduler.start()

# Ensure the scheduler is shut down when the application exits
import atexit
atexit.register(lambda: scheduler.shutdown())

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

@app.get("/api/db-healthchecker")
def db_healthchecker(db: Session = Depends(get_db)):
    try:
        # Attempt to execute a simple query to check database connectivity
        db.execute("SELECT 1")
        return {"message": "Database is healthy"}
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database is not reachable")

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    try:
        #Make a GET request to the JSONPlaceholder API
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        #Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="API call failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@app.get('/crypto-price-ethereum')
async def get_crypto_price():
    try:
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        url = (
            "https://api.coingecko.com/api/v3/simple/token_price/ethereum"
            "?contract_addresses=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
            f"&vs_currencies=usd&x_cg_demo_api_key={api_key}"
        )
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="API call failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
