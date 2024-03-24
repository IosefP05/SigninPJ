from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

# Create FastAPI app instance
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Connect to the database
DATABASE_URL = "postgresql://postgres:postgres@localhost/ptRAUL"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define SQLAlchemy Base
Base = declarative_base()

# Define ORM model for the Users table
class UserData(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

# Create the Users table in the database
Base.metadata.create_all(bind=engine)
print("-I- Table created successfully")

# Pydantic model for request body validation
class UserModel(BaseModel):
    email: str
    password: str

# Route to serve index.html
@app.get("/")
async def get_index():
    return FileResponse("index.html")

# Route to add data to the Users table
@app.post("/add-data")
def add_data(user_data: UserModel, db: Session = Depends(get_db)):
    try:
        print("Received data:", user_data)
        db_user = UserData(email=user_data.email, password=user_data.password)
        print("Adding user to database:", db_user)
        db.add(db_user)
        db.commit()
        print("User added successfully")
        db.refresh(db_user)
        return {"message": "Data added successfully"}
    except SQLAlchemyError as e:
        # Print error message
        print("Error occurred during data insertion:", str(e))
        
        # Return error response
        raise HTTPException(status_code=500, detail="An error occurred while adding data to the database")