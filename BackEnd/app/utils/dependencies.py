from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM
from bson import ObjectId
from app.database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Ejemplo: { "sub": "id", "role": "administrator", "exp": ... }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_db(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        # Busca en admin, technicians o users
        collections = ["administrators", "technicians", "users"]
        user = None
        for col in collections:
            found = await db[col].find_one({"_id": ObjectId(user_id)})
            if found:
                found["_id"] = str(found["_id"])
                found["id"] = found["_id"]
                user = found
                break

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
