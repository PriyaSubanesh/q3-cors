import time
import uuid

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-0yu8h3.example.com"
EMAIL = "24f3003806@ds.study.iitm.ac.in"

# Permit browser requests from only the assigned origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Add both required headers to every response, including errors and preflights.
@app.middleware("http")
async def add_required_headers(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed = max(0.0, time.perf_counter() - start_time)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    return response


@app.get("/stats")
async def get_stats(values: str = Query(...)):
    try:
        numbers = [int(item.strip()) for item in values.split(",")]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="values must be comma-separated integers",
        )

    if not numbers:
        raise HTTPException(status_code=400, detail="provide at least one integer")

    total = sum(numbers)

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }