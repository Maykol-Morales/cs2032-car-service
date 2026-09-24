# cs2032-car-service

> Proyecto del curso **CS2032 – Cloud Computing** · UTEC · 2024-1

Microservicio REST para el catálogo de autos, construido con **FastAPI** y **MongoDB**. Forma parte de un backend de tres microservicios:

| Servicio | Puerto | Responsabilidad |
|---|---|---|
| [cs2032-user-service](https://github.com/maykol-morales/cs2032-user-service) | 8001 | Usuarios, registro y login |
| **cs2032-car-service** | 8002 | Catálogo de autos |
| [cs2032-purchase-service](https://github.com/maykol-morales/cs2032-purchase-service) | 8003 | Compras (marca el auto como no disponible) |

## Stack

- Python 3.12 · FastAPI · Pydantic
- MongoDB (`pymongo`), base `car`, colección `production`
- Docker

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/car` | Crea un auto y devuelve su ID (UUID) |
| `GET` | `/car/{car_id}` | Obtiene un auto |
| `PUT` | `/car/{car_id}` | Actualiza un auto |
| `DELETE` | `/car/{car_id}` | Elimina un auto |
| `GET` | `/cars/` | Lista todos los autos |

La documentación interactiva queda disponible en `/docs` (Swagger UI).

### Modelo `Car`

```json
{
  "brand": "Toyota",
  "model": "Corolla",
  "color": "Blanco",
  "description": "Sedán compacto",
  "year": 2022,
  "type": "sedan",
  "image": "https://...",
  "price": 25000,
  "available": true
}
```

## Ejecución

Requiere MongoDB escuchando en `localhost:27017`.

```bash
# MongoDB local
docker run -d --name mongo -p 27017:27017 mongo

# Local
pip install -r requirements.txt
fastapi dev main.py --port 8002

# Docker (usa la red del host para alcanzar MongoDB en localhost)
docker build -t car-service .
docker run --network host car-service
```

## Licencia

[Apache 2.0](LICENSE)
