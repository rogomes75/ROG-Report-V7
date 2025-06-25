from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import logging
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection - with error handling
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ.get('DATABASE_URL', os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
    db_name = os.environ.get('DB_NAME', 'pool_maintenance_db')
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    mongodb_available = True
    logger.info("MongoDB connection initialized successfully")
except Exception as e:
    logger.error(f"MongoDB connection error: {e}")
    mongodb_available = False
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
    status: str = "reported"
    priority: str = "NORMAL"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

@app.get("/")
def read_root():
    return {
        "message": "ROG Pool Service is running with MongoDB!", 
        "status": "OK", 
        "version": "2.0",
        "database": "connected" if mongodb_available else "disconnected",
        "mongodb_available": mongodb_available
    }

@app.get("/api/")
def api_root():
    return {
        "message": "ROG Pool Service API with Database", 
        "status": "healthy", 
        "endpoints": ["/", "/api/", "/health", "/clients", "/reports"],
        "database": "connected" if mongodb_available else "disconnected"
    }

@app.get("/health")
async def health_check():
    db_status = "disconnected"
    db_details = {"configured": mongodb_available, "connection_url": bool(os.environ.get('DATABASE_URL'))}
    
    if mongodb_available and db:
        try:
            # Test database connection
            await db.test_collection.find_one()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
            db_details["error"] = str(e)
    
    return {
        "status": "healthy", 
        "service": "rog-pool-service", 
        "database": db_status,
        "database_details": db_details,
        "port": os.environ.get("PORT", "8000")
    }

@app.get("/test")
def test_endpoint():
    return {
        "message": "Test endpoint working!", 
        "railway": "deployed",
        "mongodb": "integrated" if mongodb_available else "not_available",
        "collections": ["clients", "service_reports", "users"] if mongodb_available else []
    }

# MongoDB Collections Endpoints
@app.get("/api/clients")
async def get_clients():
    if not mongodb_available or not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        clients = []
        async for client in db.clients.find():
            client['_id'] = str(client['_id'])
            clients.append(client)
        return clients
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching clients: {str(e)}")

@app.post("/api/clients")
async def create_client(client: Client):
    if not mongodb_available or not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        client_dict = client.dict()
        result = await db.clients.insert_one(client_dict)
        logger.info(f"Client created with ID: {client.id}")
        return client
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating client: {str(e)}")

@app.get("/api/reports")
async def get_reports():
    if not mongodb_available or not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        reports = []
        async for report in db.service_reports.find():
            report['_id'] = str(report['_id'])
            reports.append(report)
        return reports
    except Exception as e:
        logger.error(f"Error fetching reports: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching reports: {str(e)}")

@app.post("/api/reports")
async def create_report(report: ServiceReport):
    if not mongodb_available or not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        report_dict = report.dict()
        result = await db.service_reports.insert_one(report_dict)
        logger.info(f"Service report created with ID: {report.id}")
        return report
    except Exception as e:
        logger.error(f"Error creating report: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating report: {str(e)}")

@app.post("/api/init-data")
async def initialize_sample_data():
    if not mongodb_available or not db:
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
        
        await db.clients.insert_many(sample_clients)
        
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
        raise HTTPException(status_code=500, detail=f"Error initializing sample data: {str(e)}")

@app.get("/html", response_class=HTMLResponse)
def html_page():
    return f"""
    <html>
        <head><title>ROG Pool Service - MongoDB Integration</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🏊‍♂️ ROG Pool Service</h1>
            <h2>✅ API with MongoDB Integration</h2>
            <p><strong>Status:</strong> Running successfully!</p>
            <p><strong>MongoDB:</strong> {'✅ Available' if mongodb_available else '❌ Not Available'}</p>
            
            <h3>🔗 API Endpoints:</h3>
            <ul>
                <li><a href="/api/">API Root</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/test">Test Endpoint</a></li>
                {"<li><a href='/api/clients'>View Clients</a></li>" if mongodb_available else ""}
                {"<li><a href='/api/reports'>View Reports</a></li>" if mongodb_available else ""}
                {"<li><a href='#' onclick='initData()'>Initialize Sample Data</a></li>" if mongodb_available else ""}
            </ul>
            
            <h3>🗄️ Database Features:</h3>
            <ul>
                <li>{'✅' if mongodb_available else '❌'} MongoDB Connection</li>
                <li>{'✅' if mongodb_available else '❌'} Clients Management</li>
                <li>{'✅' if mongodb_available else '❌'} Service Reports</li>
                <li>{'✅' if mongodb_available else '❌'} Sample Data Creation</li>
            </ul>
            
            <script>
                function initData() {{
                    fetch('/api/init-data', {{method: 'POST'}})
                        .then(response => response.json())
                        .then(data => alert(JSON.stringify(data, null, 2)))
                        .catch(error => alert('Error: ' + error));
                }}
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)