# mock_api/status_server.py
from fastapi import FastAPI
from prometheus_client import make_asgi_app
import time

app = FastAPI(title="Agent X Status Monitor")

# Add Prometheus metrics route
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
def health_check():
    """Returns the simulated health of the local AI components."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "components": {
            "whisper_transcriber": "online",
            "ollama_reasoning_engine": "online",
            "wayland_scanner": "idle"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
