from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import jwt
from passlib.context import CryptContext
import base64
import pandas as pd
from io import BytesIO

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
SECRET_KEY = "pool_maintenance_secret_key_2024"
ALGORITHM = "HS256"
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    role: str  # "admin" or "employee"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "employee"

class UserLogin(BaseModel):
    username: str
    password: str

class Client(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    address: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ServiceReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str
    client_name: str
    employee_id: str
    employee_name: str
    description: str
    photos: List[str] = []  # base64 encoded images
    priority: str  # "URGENT", "SAME WEEK", "NEXT WEEK"
    status: str = "reported"  # "reported", "scheduled", "in_progress", "completed"
    request_date: datetime = Field(default_factory=datetime.utcnow)
    completion_date: Optional[datetime] = None
    admin_notes: str = ""
    employee_notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_time: str = Field(default_factory=lambda: datetime.utcnow().strftime("%H:%M"))
    last_modified: datetime = Field(default_factory=datetime.utcnow)
    modification_history: List[dict] = []

class ServiceReportCreate(BaseModel):
    client_id: str
    description: str
    photos: List[str] = []
    priority: str

class ServiceReportUpdate(BaseModel):
    status: Optional[str] = None
    admin_notes: Optional[str] = None
    employee_notes: Optional[str] = None
    completion_date: Optional[datetime] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    photos: Optional[List[str]] = None

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = await db.users.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Initialize admin user
@app.on_event("startup")
async def startup_event():
    # Check if admin user exists, if not create one
    admin_user = await db.users.find_one({"username": "admin"})
    if not admin_user:
        admin_user_data = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "password_hash": get_password_hash("admin123"),
            "role": "admin",
            "created_at": datetime.utcnow()
        }
        await db.users.insert_one(admin_user_data)
        logging.info("Admin user created")

# Auth routes
@api_router.post("/auth/login")
async def login(user_data: UserLogin):
    user = await db.users.find_one({"username": user_data.username})
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }

@api_router.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# User management routes (admin only)
@api_router.post("/users", response_model=User)
async def create_user(user_data: UserCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_dict = user_data.dict()
    user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
    user_dict["id"] = str(uuid.uuid4())
    user_dict["created_at"] = datetime.utcnow()
    
    await db.users.insert_one(user_dict)
    return User(**user_dict)

@api_router.get("/users", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view users")
    
    users = await db.users.find().to_list(1000)
    return [User(**user) for user in users]

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")
    
    result = await db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Client routes
@api_router.delete("/clients/{client_id}")
async def delete_client(client_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete clients")
    
    result = await db.clients.delete_one({"id": client_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}

@api_router.post("/clients/import-excel")
async def import_clients_excel(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can import clients")
    
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))
        
        # Assuming Excel has columns: 'Name' and 'Address'
        clients_data = []
        for _, row in df.iterrows():
            client_data = {
                "id": str(uuid.uuid4()),
                "name": str(row['Name']) if 'Name' in row else str(row['name']),
                "address": str(row['Address']) if 'Address' in row else str(row['address']),
                "created_at": datetime.utcnow()
            }
            clients_data.append(client_data)
        
        if clients_data:
            await db.clients.insert_many(clients_data)
        
        return {"message": f"Successfully imported {len(clients_data)} clients"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing Excel file: {str(e)}")

@api_router.get("/clients", response_model=List[Client])
async def get_clients(current_user: User = Depends(get_current_user)):
    clients = await db.clients.find().sort("name", 1).to_list(1000)  # Alphabetical order
    return [Client(**client) for client in clients]

@api_router.post("/clients", response_model=Client)
async def create_client(client_data: dict, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create clients")
    
    client_dict = {
        "id": str(uuid.uuid4()),
        "name": client_data["name"],
        "address": client_data["address"],
        "created_at": datetime.utcnow()
    }
    
    await db.clients.insert_one(client_dict)
    return Client(**client_dict)

# Service report routes
@api_router.post("/reports", response_model=ServiceReport)
async def create_service_report(report_data: ServiceReportCreate, current_user: User = Depends(get_current_user)):
    # Get client info
    client = await db.clients.find_one({"id": report_data.client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    report_dict = report_data.dict()
    report_dict["id"] = str(uuid.uuid4())
    report_dict["client_name"] = client["name"]
    report_dict["employee_id"] = current_user.id
    report_dict["employee_name"] = current_user.username
    report_dict["status"] = "reported"
    report_dict["admin_notes"] = ""
    report_dict["created_at"] = datetime.utcnow()
    report_dict["request_date"] = datetime.utcnow()
    
    await db.service_reports.insert_one(report_dict)
    return ServiceReport(**report_dict)

@api_router.get("/reports", response_model=List[ServiceReport])
async def get_service_reports(current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        # Admin can see all reports
        reports = await db.service_reports.find().sort("created_at", -1).to_list(1000)
    else:
        # Employees can only see their own reports
        reports = await db.service_reports.find({"employee_id": current_user.id}).sort("created_at", -1).to_list(1000)
    
    return [ServiceReport(**report) for report in reports]

@api_router.put("/reports/{report_id}", response_model=ServiceReport)
async def update_service_report(report_id: str, update_data: ServiceReportUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update reports")
    
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    
    result = await db.service_reports.update_one(
        {"id": report_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    
    updated_report = await db.service_reports.find_one({"id": report_id})
    return ServiceReport(**updated_report)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()