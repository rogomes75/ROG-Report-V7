from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ROG Pool Service API")

# Global variables for MongoDB
mongodb_available = False
client = None
db = None

@app.on_event("startup")
async def startup_event():
    global mongodb_available, client, db
    
    try:
        # Try to import and connect to MongoDB
        from motor.motor_asyncio import AsyncIOMotorClient
        mongo_url = os.environ.get('DATABASE_URL', os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
        db_name = os.environ.get('DB_NAME', 'pool_maintenance_db')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Test connection
        await db.test_collection.find_one()
        mongodb_available = True
        logger.info("MongoDB connection successful")
        
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        mongodb_available = False
        client = None
        db = None

@app.get("/")
def read_root():
    return {
        "message": "ROG Pool Service is running with MongoDB support!", 
        "status": "OK", 
        "version": "2.1",
        "database": "connected" if mongodb_available else "disconnected",
        "mongodb_available": mongodb_available
    }

@app.get("/api/")
def api_root():
    return {
        "message": "ROG Pool Service API", 
        "status": "healthy", 
        "endpoints": ["/", "/api/", "/health", "/test"],
        "mongodb_endpoints": ["/api/clients", "/api/reports", "/api/init-data"] if mongodb_available else [],
        "database": "connected" if mongodb_available else "disconnected"
    }

@app.get("/health")
async def health_check():
    db_status = "disconnected"
    db_details = {
        "mongodb_available": mongodb_available,
        "environment_vars": {
            "DATABASE_URL": bool(os.environ.get('DATABASE_URL')),
            "MONGO_URL": bool(os.environ.get('MONGO_URL')),
            "DB_NAME": os.environ.get('DB_NAME', 'pool_maintenance_db')
        }
    }
    
    if mongodb_available and db:
        try:
            await db.test_collection.find_one()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
            db_details["connection_error"] = str(e)
    
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
        "mongodb": "available" if mongodb_available else "not_available",
        "version": "2.1"
    }

# MongoDB endpoints - only work if MongoDB is available
@app.get("/api/clients")
async def get_clients():
    if not mongodb_available:
        return {"message": "MongoDB not available", "clients": []}
    
    try:
        clients = []
        async for client in db.clients.find():
            client['_id'] = str(client['_id'])
            clients.append(client)
        return {"clients": clients, "count": len(clients)}
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        return {"error": str(e), "clients": []}

@app.get("/api/reports")
async def get_reports():
    if not mongodb_available:
        return {"message": "MongoDB not available", "reports": []}
    
    try:
        reports = []
        async for report in db.service_reports.find():
            report['_id'] = str(report['_id'])
            reports.append(report)
        return {"reports": reports, "count": len(reports)}
    except Exception as e:
        logger.error(f"Error fetching reports: {e}")
        return {"error": str(e), "reports": []}

@app.post("/api/init-data")
async def initialize_sample_data():
    if not mongodb_available:
        return {"error": "MongoDB not available"}
    
    try:
        import uuid
        from datetime import datetime
        
        # Check if data exists
        client_count = await db.clients.count_documents({})
        if client_count > 0:
            return {"message": "Sample data already exists", "clients": client_count}
        
        # Create sample data
        sample_clients = [
            {
                "id": str(uuid.uuid4()),
                "name": "João Silva",
                "address": "Rua das Flores, 123",
                "phone": "(11) 99999-9999",
                "email": "joao@email.com",
                "created_at": datetime.now()
            }
        ]
        
        await db.clients.insert_many(sample_clients)
        
        return {
            "message": "Sample data created successfully!",
            "clients_created": len(sample_clients)
        }
    except Exception as e:
        logger.error(f"Error initializing data: {e}")
        return {"error": str(e)}

@app.get("/html", response_class=HTMLResponse)
def html_page():
    return f"""
    <html>
        <head><title>ROG Pool Service v2.1</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🏊‍♂️ ROG Pool Service v2.1</h1>
            <h2>✅ Railway Deploy Successful</h2>
            
            <div style="background: {'#d4edda' if mongodb_available else '#f8d7da'}; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>🗄️ MongoDB Status: {'✅ Connected' if mongodb_available else '❌ Not Available'}</h3>
            </div>
            
            <h3>🔗 API Endpoints (Always Available):</h3>
            <ul>
                <li><a href="/">Root</a></li>
                <li><a href="/api/">API Root</a></li>
                <li><a href="/health">Health Check (Detailed)</a></li>
                <li><a href="/test">Test Endpoint</a></li>
            </ul>
            
            {f'''
            <h3>🗄️ MongoDB Endpoints (Available):</h3>
            <ul>
                <li><a href="/api/clients">View Clients</a></li>
                <li><a href="/api/reports">View Reports</a></li>
                <li><a href="#" onclick="initData()">Initialize Sample Data</a></li>
            </ul>
            ''' if mongodb_available else '<h3>🗄️ MongoDB Endpoints: Not Available</h3>'}
            
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