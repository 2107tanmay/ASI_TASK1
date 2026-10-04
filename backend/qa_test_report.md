# Backend QA & Adversarial Test Report

## Endpoints Discovered

- **GET** `/api/health`: Health Check
- **GET** `/api/decision-pack`: Get Decision Pack
- **POST** `/api/documents/upload`: Upload Document
- **GET** `/api/evidence`: List Evidence
- **GET** `/api/evidence/{evidence_id}`: Get Evidence
- **POST** `/api/calculations/run`: Run Calculation
- **GET** `/api/calculations/{run_id}`: Get Calculation

## Test Executions

### GET /health

- **Status**: 200
- **Response**: `{"status": "ok"}`
- **Result**: PASS

### GET /decision-pack

- **Status**: 200
- **Response**: `{"status": "ok", "message": "decision pack placeholder"}`
- **Result**: PASS

### GET /evidence

- **Status**: 200
- **Response**: `[]`
- **Result**: PASS

### GET /evidence/1

- **Status**: 404
- **Error Body**: `{"detail":"Evidence not found"}`
- **Result**: CAUGHT ERROR (Expected for empty/invalid data)

### POST /calculations/run

- **Status**: 422
- **Error Body**: `{"detail":[{"type":"missing","loc":["body"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.13/v/missing"}]}`
- **Result**: CAUGHT ERROR (Expected for empty/invalid data)

### POST /documents/upload

- **Status**: 422
- **Error Body**: `{"detail":[{"type":"missing","loc":["body","file"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.13/v/missing"}]}`
- **Result**: CAUGHT ERROR (422 Expected)
