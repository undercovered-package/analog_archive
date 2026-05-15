from fastapi import APIRouter
from tortoise import connections

router = APIRouter()


@router.get("/health")
async def health_check():
    try:
        conn = connections.get("default")
        await conn.execute_query("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return {"status": "ok", "database": db_status}
