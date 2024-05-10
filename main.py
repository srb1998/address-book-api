from fastapi import FastAPI,Depends, HTTPException, status
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from typing import List
import models, schemas
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(connect_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def root():
    return {"message": "Welcome to Address Book API."}

@app.post("/signup/", response_model=schemas.UserInDB)
def signup(user: schemas.UserCreate, db: Session = Depends(connect_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    # Hashing password
    hashed_password = pwd_context.hash(user.password)
    # Creating new user
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(connect_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(connect_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
        
@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(connect_db), current_user: models.User = Depends(get_current_user)):
    db_address = models.Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(db: Session = Depends(connect_db), current_user: models.User = Depends(get_current_user)):
    addresses = db.query(models.Address).all()
    return addresses

@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(connect_db), current_user: models.User = Depends(get_current_user)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressCreate, db: Session = Depends(connect_db), current_user: models.User = Depends(get_current_user)):
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
def delete_address(address_id: int, db: Session = Depends(connect_db), current_user: models.User = Depends(get_current_user)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return None

@app.get("/addresses/nearby/", response_model=List[schemas.Address])
def read_nearby_addresses(latitude: float, longitude: float, distance: float, db: Session = Depends(connect_db), current_user: models.User = Depends(get_current_user)):
    addresses = db.query(models.Address).all()
    nearby_addresses = []
    location = (latitude, longitude)
    for address in addresses:
        address_location = (address.latitude, address.longitude)
        if geodesic(location, address_location).km <= distance:
            nearby_addresses.append(address)
    return nearby_addresses