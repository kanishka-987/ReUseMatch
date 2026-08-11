# ReUseMatch API Reference

This document outlines the REST API endpoints provided by the FastAPI backend server.

## Base URL
By default, the server runs locally on:
`http://127.0.0.1:8000`

---

## Endpoints

### 1. Root Welcome
Returns a welcome message indicating API status and link to docs.

- **Method**: `GET`
- **Path**: `/`
- **Response**: `200 OK`
  ```json
  {
    "message": "Welcome to the ReUseMatch API",
    "docs": "/docs",
    "status": "active"
  }
  ```

---

### 2. Liveness / Health Check
Checks backend health status and active configuration.

- **Method**: `GET`
- **Path**: `/health`
- **Response**: `200 OK`
  ```json
  {
    "status": "healthy",
    "environment": "development"
  }
  ```

---

### 3. Run Matching Sequence
Triggers the multi-agent orchestration pipeline to match a newly submitted item.

- **Method**: `POST`
- **Path**: `/api/matches/`
- **Request Body**:
  ```json
  {
    "name": "Wooden dining table",
    "description": "Solid oak kitchen table. Dimensions 150x90cm. Light surface wear on top.",
    "image_url": "https://example.com/images/table.jpg",
    "location": "742 Evergreen Terrace, Springfield"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "item_name": "Generic Wooden Table",
    "category": "Furniture",
    "condition": "Good",
    "status": "matched",
    "matches": [
      {
        "recipient": {
          "organization_id": "org_001",
          "organization_name": "Community Housing Shelter",
          "priority": "High"
        },
        "logistics": {
          "origin": "742 Evergreen Terrace, Springfield",
          "destination": "Community Housing Shelter Center, Downtown",
          "distance_km": 12.5,
          "estimated_cost_usd": 18.75,
          "recommended_mode": "Local Pickup Courier"
        },
        "score": 7.0
      }
    ]
  }
  ```

---

### 4. Get Match Details
Gets details or history for a specific item's match run.

- **Method**: `GET`
- **Path**: `/api/matches/{item_id}`
- **Response**: `200 OK`
  ```json
  {
    "item_id": "item_123_placeholder",
    "status": "completed",
    "matched_recipient_id": "org_456_shelter",
    "logistics_route": "Direct Pickup - Route A",
    "confidence_score": 0.95
  }
  ```
- **Response Status Errors**:
  - `404 Not Found`: Returned when no entry matches the `item_id`.
