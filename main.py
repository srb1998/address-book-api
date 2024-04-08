from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from typing import List
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(connect_db)):
    db_address = models.Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(db: Session = Depends(connect_db)):
    addresses = db.query(models.Address).all()
    return addresses

@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(connect_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressCreate, db: Session = Depends(connect_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db_address.name = address.name
    db_address.latitude = address.latitude
    db_address.longitude = address.longitude
    db.commit()
    db.refresh(db_address)
    return db_address

@app.delete("/addresses/{address_id}", response_model=None)
def delete_address(address_id: int, db: Session = Depends(connect_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return None

@app.get("/addresses/nearby/", response_model=List[schemas.Address])
def read_nearby_addresses(latitude: float, longitude: float, distance: float, db: Session = Depends(connect_db)):
    addresses = db.query(models.Address).all()
    nearby_addresses = []
    location = (latitude, longitude)
    for address in addresses:
        address_location = (address.latitude, address.longitude)
        if geodesic(location, address_location).km <= distance:
            nearby_addresses.append(address)
    return nearby_addresses