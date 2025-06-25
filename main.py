from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ROG Pool Service is running!", "status": "OK", "version": "1.0"}

@app.get("/api/")
def api_root():
    return {"message": "ROG Pool Service API", "status": "healthy", "endpoints": ["/", "/api/", "/health"]}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rog-pool-service", "port": os.environ.get("PORT", "8000")}

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working!", "railway": "deployed"}

# Serve a simple HTML page for browser testing
@app.get("/html", response_class=HTMLResponse)
def html_page():
    return """
    <html>
        <head><title>ROG Pool Service</title></head>
        <body>
            <h1>🏊‍♂️ ROG Pool Service</h1>
            <p>✅ API is running successfully!</p>
            <ul>
                <li><a href="/api/">API Root</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/test">Test Endpoint</a></li>
            </ul>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)