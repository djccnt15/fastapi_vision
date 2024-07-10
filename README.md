# ocr_backend
FastAPI 기반 OCR Backend 서버

## memo

- commends for running FastAPI dev server

```powershell
fastapi dev main.py
```

- commends for running uvicorn server for debugging

```powershell
main.py
```

## alembic migration

- initialize alembic

```powershell
alembic init migrations
```

- create revision

```powershell
alembic revision --autogenerate
```

- run migration to latest revision

```powershell
alembic upgrade head
```

## Docker

- Dockerfile build

```
docker build -t fastocr .
```

- Docker container run

```
docker run -itd -p 8000:8000 --name fastocr fastocr
```