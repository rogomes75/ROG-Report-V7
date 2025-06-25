from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import logging
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ.get('DATABASE_URL', os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db_name = os.environ.get('DB_NAME', 'pool_maintenance_db')

try:
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    logger.info("MongoDB connection initialized successfully")
except Exception as e:
    logger.error(f"MongoDB connection error: {e}")
    client = None
    db = None

app = FastAPI(title="ROG Pool Service API with MongoDB")

# Pydantic Models
class Client(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class ServiceReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str
    title: str
    description: str
    status: str = "reported"  # reported, scheduled, in_progress, completed
    priority: str = "NORMAL"  # URGENT, SAME_WEEK, NEXT_WEEK, NORMAL
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

@app.get("/")
def read_root():
    return {
        "message": "ROG Pool Service is running with MongoDB!", 
        "status": "OK", 
        "version": "2.0",
        "database": "connected" if db else "disconnected"
    }

@app.get("/api/")
def api_root():
    return {
        "message": "ROG Pool Service API with Database", 
        "status": "healthy", 
        "endpoints": ["/", "/api/", "/health", "/clients", "/reports"],
        "database": "connected" if db else "disconnected"
    }

@app.get("/health")
async def health_check():
    db_status = "disconnected"
    if db:
        try:
            # Test database connection
            await db.test_collection.find_one()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy", 
        "service": "rog-pool-service", 
        "database": db_status,
        "mongodb_url_configured": bool(mongo_url),
        "port": os.environ.get("PORT", "8000")
    }

@app.get("/test")
def test_endpoint():
    return {
        "message": "Test endpoint working!", 
        "railway": "deployed",
        "mongodb": "integrated",
        "collections": ["clients", "service_reports", "users"]
    }

# MongoDB Collections Endpoints
@app.get("/api/clients", response_model=List[Client])
async def get_clients():
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        clients = []
        async for client in db.clients.find():
            client['_id'] = str(client['_id'])  # Convert ObjectId to string
            clients.append(Client(**client))
        return clients
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        raise HTTPException(status_code=500, detail="Error fetching clients")

@app.post("/api/clients", response_model=Client)
async def create_client(client: Client):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        client_dict = client.dict()
        result = await db.clients.insert_one(client_dict)
        logger.info(f"Client created with ID: {client.id}")
        return client
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        raise HTTPException(status_code=500, detail="Error creating client")

@app.get("/api/reports", response_model=List[ServiceReport])
async def get_reports():
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        reports = []
        async for report in db.service_reports.find():
            report['_id'] = str(report['_id'])  # Convert ObjectId to string
            reports.append(ServiceReport(**report))
        return reports
    except Exception as e:
        logger.error(f"Error fetching reports: {e}")
        raise HTTPException(status_code=500, detail="Error fetching reports")

@app.post("/api/reports", response_model=ServiceReport)
async def create_report(report: ServiceReport):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        report_dict = report.dict()
        result = await db.service_reports.insert_one(report_dict)
        logger.info(f"Service report created with ID: {report.id}")
        return report
    except Exception as e:
        logger.error(f"Error creating report: {e}")
        raise HTTPException(status_code=500, detail="Error creating report")

# Create sample data endpoint
@app.post("/api/init-data")
async def initialize_sample_data():
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Check if data already exists
        client_count = await db.clients.count_documents({})
        if client_count > 0:
            return {"message": "Sample data already exists", "clients": client_count}
        
        # Create sample clients
        sample_clients = [
            {
                "id": str(uuid.uuid4()),
                "name": "João Silva",
                "address": "Rua das Flores, 123",
                "phone": "(11) 99999-9999",
                "email": "joao@email.com",
                "created_at": datetime.now()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Maria Santos",
                "address": "Av. Paulista, 456",
                "phone": "(11) 88888-8888",
                "email": "maria@email.com",
                "created_at": datetime.now()
            }
        ]
        
        # Insert sample clients
        await db.clients.insert_many(sample_clients)
        
        # Create sample service report
        sample_report = {
            "id": str(uuid.uuid4()),
            "client_id": sample_clients[0]["id"],
            "title": "Limpeza da Piscina",
            "description": "Limpeza geral da piscina e verificação dos equipamentos",
            "status": "reported",
            "priority": "NORMAL",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        await db.service_reports.insert_one(sample_report)
        
        return {
            "message": "Sample data created successfully!",
            "clients_created": len(sample_clients),
            "reports_created": 1
        }
    except Exception as e:
        logger.error(f"Error initializing data: {e}")
        raise HTTPException(status_code=500, detail="Error initializing sample data")

# Serve a simple HTML page for browser testing
@app.get("/html", response_class=HTMLResponse)
def html_page():
    return """
    <html>
        <head><title>ROG Pool Service - MongoDB Integration</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🏊‍♂️ ROG Pool Service</h1>
            <h2>✅ API with MongoDB Integration</h2>
            <p><strong>Status:</strong> Running successfully!</p>
            
            <h3>🔗 API Endpoints:</h3>
            <ul>
                <li><a href="/api/">API Root</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/test">Test Endpoint</a></li>
                <li><a href="/api/clients">View Clients</a></li>
                <li><a href="/api/reports">View Reports</a></li>
                <li><a href="/api/init-data" onclick="initData()">Initialize Sample Data</a></li>
            </ul>
            
            <h3>🗄️ Database Features:</h3>
            <ul>
                <li>✅ MongoDB Connection</li>
                <li>✅ Clients Management</li>
                <li>✅ Service Reports</li>
                <li>✅ Sample Data Creation</li>
            </ul>
            
            <script>
                function initData() {
                    fetch('/api/init-data', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => alert(JSON.stringify(data, null, 2)))
                        .catch(error => alert('Error: ' + error));
                }
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)