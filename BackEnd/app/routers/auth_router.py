from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.utils.auth import verify_password, create_access_token
from app.database import db

router = APIRouter()

@router.post("/login", response_model=TokenResponse, summary="Login general")
async def login(login_data: LoginRequest):
    collections = ["administrators", "technicians", "users"]

    user = None
    for col in collections:
        user = await db[col].find_one({"email": login_data.email})
        if user:
            break

    if not user or user.get("status") != "active":
        raise HTTPException(status_code=401, detail="Credenciales inválidas o usuario inactivo")

    if not verify_password(login_data.password, user["salt"], user["passwordHash"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {
        "sub": str(user["_id"]),
        "role": user["role"],
        "email": user["email"]
    }

    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}
