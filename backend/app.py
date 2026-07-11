from fastapi import FastAPI

app = FastAPI(
    title="HobbyFi Copilot",
    version="1.0.0",
    description="AI CRM Assistant for Vendor Portal"
)

@app.get("/")
def root():
    return {
        "message": "HobbyFi Copilot Backend is Running 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }