from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "ROG Pool Service - Basic Version", 
        "status": "OK", 
        "version": "1.5",
        "info": "MongoDB integration will be added after basic version works"
    }

@app.get("/api/")
def api_root():
    return {
        "message": "ROG Pool Service API", 
        "status": "healthy", 
        "endpoints": ["/", "/api/", "/health", "/test"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "rog-pool-service",
        "port": os.environ.get("PORT", "8000"),
        "environment_vars": {
            "DATABASE_URL": "present" if os.environ.get('DATABASE_URL') else "missing",
            "DB_NAME": os.environ.get('DB_NAME', 'not_set')
        }
    }

@app.get("/test")
def test_endpoint():
    return {
        "message": "Test endpoint working!", 
        "railway": "deployed",
        "version": "1.5",
        "mongodb_status": "will_be_added_next"
    }

@app.get("/html", response_class=HTMLResponse)
def html_page():
    env_vars = {
        "DATABASE_URL": os.environ.get('DATABASE_URL', 'Not set'),
        "DB_NAME": os.environ.get('DB_NAME', 'Not set'),
        "PORT": os.environ.get('PORT', 'Not set')
    }
    
    return f"""
    <html>
        <head><title>ROG Pool Service - Debug Version</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🏊‍♂️ ROG Pool Service v1.5</h1>
            <h2>✅ Basic Version Working</h2>
            
            <h3>🔗 Working Endpoints:</h3>
            <ul>
                <li><a href="/">Root</a></li>
                <li><a href="/api/">API Root</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/test">Test Endpoint</a></li>
            </ul>
            
            <h3>🔍 Environment Variables:</h3>
            <ul>
                {"".join([f"<li><strong>{key}:</strong> {'✅ Set' if value != 'Not set' else '❌ Not set'}</li>" for key, value in env_vars.items()])}
            </ul>
            
            <h3>📝 Next Steps:</h3>
            <ol>
                <li>✅ Basic FastAPI working</li>
                <li>🔄 Add MongoDB integration</li>
                <li>⏳ Add authentication</li>
                <li>⏳ Add pool service features</li>
            </ol>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)