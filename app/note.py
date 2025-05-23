from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response

from .database import get_db
import requests
import os
import app
from app.utils import get_coin_id
# from dotenv import load_dotenv # removed for Docker

# load_dotenv() # removed for Docker

router = APIRouter()



@router.get('/')
def get_notes(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    notes = db.query(models.Note).filter(
        models.Note.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(notes), 'notes': notes}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    try:
        # Get the API key
        api_key = os.getenv("API_KEY") #locally might be api_key, in docker it is API_KEY
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        # Retrieve the CoinGecko coin ID using the payload title
        coin_id = get_coin_id(payload.title)
        
        # Build the API URL using the retrieved coin ID
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={coin_id}"
            f"&vs_currencies=usd"
            f"&x_cg_demo_api_key={api_key}"
        )

        # Make the request to get the crypto price
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="API call failed")

        data = response.json()
        price = data.get(coin_id, {}).get("usd")

        if price is None:
            raise HTTPException(status_code=500, detail="Invalid response from crypto API")

        # Create the note with the title from the payload and content as the crypto price
        new_note = models.Note(
            title=payload.title,
            content=f"Current {payload.title} price (USD):\n${price}",
            category=payload.category,
            published=payload.published
        )

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        return {"status": "success", "note": new_note}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.patch('/{noteId}')
def update_note(noteId: str, payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {noteId} found')

    update_data = payload.dict(exclude_unset=True)

    try:
        # If the title is being updated, also update the content (crypto price)
        if "title" in update_data:
            api_key = os.getenv("API_KEY")
            if not api_key:
                raise HTTPException(status_code=500, detail="API key not configured")

            coin_id = get_coin_id(update_data["title"])

            url = (
                f"https://api.coingecko.com/api/v3/simple/price"
                f"?ids={coin_id}"
                f"&vs_currencies=usd"
                f"&x_cg_demo_api_key={api_key}"
            )

            response = requests.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="API call failed")

            data = response.json()
            price = data.get(coin_id, {}).get("usd")

            if price is None:
                raise HTTPException(status_code=500, detail="Invalid response from crypto API")

            update_data["content"] = f"Current {update_data['title']} price (USD):\n${price}"

        note_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_note)

        return {"status": "success", "note": db_note}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/{noteId}')
def get_post(noteId: str, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == noteId).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {id} found")
    return {"status": "success", "note": note}


@router.delete('/{noteId}')
def delete_post(noteId: str, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
