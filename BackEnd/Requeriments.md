requerimentos para usar instalar:
- fastapi
- uvicorn
- motor
- pydantic
- bcrypt
- python-dotenv

`pip install fastapi uvicorn motor pydantic bcrypt python-dotenv`

`pip install "fastapi[standard]"`

`pip install python-jose[cryptography]`

usuario Administrador para probar:
```
{
  "name": "Sebastián",
  "lastname": "Guerrero",
  "email": "admin@ata.com",
  "password": "MiClaveSegura123",
  "status": "active"
}

```
## Tecnico para probar

```
{
  "email": "carlos@ata.com",
  "password": "passwordCarlos123"
}

```

## Usuario para probar
```
{
  "email": "luis@empresa.com",
  "password": "clave1234"   
}
```

## creacion de sensor para usuario
```
{
  "serial": "SN-12345",
  "type": "humidity",
  "location": "Bodega Central",
  "ownerUserId": "6848624415b166c895fc4783",
  "thresholds": {
    "min": 20,
    "max": 70
  }
}
```