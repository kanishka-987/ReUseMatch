# ReUseMatch Backend API Contract & Technical Documentation

This document defines the complete backend API contract for the **ReUseMatch** platform, designed for seamless integration between Team Members, Frontend applications, and AI Agent Orchestration layers.

---

## 1. General Specifications

* **Base Development URL**: `http://127.0.0.1:8000`
* **API Prefix**: `/api`
* **Data Format**: JSON (`Content-Type: application/json`)
* **ID Format**: Standard 36-character UUIDv4 strings (e.g., `b4e73869-7259-4d87-a72f-8625f72d0e7e`).
* **Authentication**: None currently required for development environment.

---

## 2. Match Scoring System Explanation

The database-driven matching engine (`backend/services/matching_service.py`) calculates a transparent, explainable match score out of **100 points**:

| Criteria | Points | Description |
| :--- | :---: | :--- |
| **Device Type Match** | **50** | **Mandatory Prerequisite**: Case-insensitive match between `device.device_type` and `recipient.required_device_type`. (Mismatched device types are excluded from matches). |
| **RAM Requirement** | **15** | Awarded if device RAM meets/exceeds recipient's `minimum_ram`, or if recipient has no RAM constraint. |
| **Storage Requirement** | **15** | Awarded if device storage meets/exceeds recipient's `minimum_storage`, or if recipient has no storage constraint. |
| **Recipient Priority** | **20 / 10 / 5** | High Priority = 20 pts \| Medium Priority = 10 pts \| Low Priority = 5 pts. |

### Score Interpretation (For Compatible Device Types)
* **85 - 100**: **Strong Match** (RAM & Storage satisfied, High/Medium priority).
* **55 - 84**: **Moderate Match** (Partial RAM/Storage satisfaction or lower priority).
* **Excluded**: Recipients with non-matching `required_device_type` are filtered out.

---

## 3. Device APIs (`/api/devices`)

### 3.1 Register Device
* **HTTP Method**: `POST`
* **URL**: `/api/devices/`
* **Purpose**: Register a new electronic device in the MySQL `devices` table.

#### Request Body
```json
{
  "device_type": "Laptop",
  "brand": "Dell",
  "model": "XPS 15",
  "year": 2022,
  "ram": "16GB",
  "storage": "512GB SSD",
  "owner_info": "Donated by TechCorp"
}
```
* **Required Fields**: `device_type`
* **Optional Fields**: `brand`, `model`, `year`, `ram`, `storage`, `owner_info`

#### Response (`201 Created`)
```json
{
  "id": "b4e73869-7259-4d87-a72f-8625f72d0e7e",
  "device_type": "Laptop",
  "brand": "Dell",
  "model": "XPS 15",
  "year": 2022,
  "ram": "16GB",
  "storage": "512GB SSD",
  "owner_info": "Donated by TechCorp",
  "created_at": "2026-08-12T06:29:56",
  "updated_at": "2026-08-12T06:29:56"
}
```

---

### 3.2 List All Devices
* **HTTP Method**: `GET`
* **URL**: `/api/devices/`
* **Purpose**: Retrieve all registered electronic devices.

#### Response (`200 OK`)
```json
[
  {
    "id": "b4e73869-7259-4d87-a72f-8625f72d0e7e",
    "device_type": "Laptop",
    "brand": "Dell",
    "model": "XPS 15",
    "year": 2022,
    "ram": "16GB",
    "storage": "512GB SSD",
    "owner_info": "Donated by TechCorp",
    "created_at": "2026-08-12T06:29:56",
    "updated_at": "2026-08-12T06:29:56"
  }
]
```

---

### 3.3 Get Device by ID
* **HTTP Method**: `GET`
* **URL**: `/api/devices/{device_id}`
* **Purpose**: Retrieve a single device by its UUID.

#### Response (`200 OK`)
```json
{
  "id": "b4e73869-7259-4d87-a72f-8625f72d0e7e",
  "device_type": "Laptop",
  "brand": "Dell",
  "model": "XPS 15",
  "year": 2022,
  "ram": "16GB",
  "storage": "512GB SSD",
  "owner_info": "Donated by TechCorp",
  "created_at": "2026-08-12T06:29:56",
  "updated_at": "2026-08-12T06:29:56"
}
```

#### Error Response (`404 Not Found`)
```json
{
  "detail": "Device with ID 'b4e73869-7259-4d87-a72f-8625f72d0e7e' not found"
}
```

---

### 3.4 Delete Device
* **HTTP Method**: `DELETE`
* **URL**: `/api/devices/{device_id}`
* **Purpose**: Delete a registered device by its UUID.

#### Response (`200 OK`)
```json
{
  "message": "Device with ID 'b4e73869-7259-4d87-a72f-8625f72d0e7e' successfully deleted",
  "id": "b4e73869-7259-4d87-a72f-8625f72d0e7e"
}
```

---

## 4. Recipient APIs (`/api/recipients`)

### 4.1 Register Recipient
* **HTTP Method**: `POST`
* **URL**: `/api/recipients/`
* **Purpose**: Register a new recipient organization or individual in the MySQL `recipients` table.

#### Request Body
```json
{
  "name": "EduTech NGO",
  "recipient_type": "NGO",
  "location": "New York, NY",
  "required_device_type": "Laptop",
  "minimum_ram": "8GB",
  "minimum_storage": "256GB",
  "quantity_needed": 5,
  "priority": "High"
}
```
* **Required Fields**: `name`, `recipient_type`, `location`, `required_device_type`
* **Optional Fields**: `minimum_ram`, `minimum_storage`, `quantity_needed` (default: 1), `priority` (default: "Medium")

#### Response (`201 Created`)
```json
{
  "id": "d74b5cd9-6226-4f38-be6c-56590fb49477",
  "name": "EduTech NGO",
  "recipient_type": "NGO",
  "location": "New York, NY",
  "required_device_type": "Laptop",
  "minimum_ram": "8GB",
  "minimum_storage": "256GB",
  "quantity_needed": 5,
  "priority": "High",
  "created_at": "2026-08-12T06:32:55",
  "updated_at": "2026-08-12T06:32:55"
}
```

---

### 4.2 List All Recipients
* **HTTP Method**: `GET`
* **URL**: `/api/recipients/`
* **Purpose**: Retrieve all registered recipients.

#### Response (`200 OK`)
```json
[
  {
    "id": "d74b5cd9-6226-4f38-be6c-56590fb49477",
    "name": "EduTech NGO",
    "recipient_type": "NGO",
    "location": "New York, NY",
    "required_device_type": "Laptop",
    "minimum_ram": "8GB",
    "minimum_storage": "256GB",
    "quantity_needed": 5,
    "priority": "High",
    "created_at": "2026-08-12T06:32:55",
    "updated_at": "2026-08-12T06:32:55"
  }
]
```

---

### 4.3 Get Recipient by ID
* **HTTP Method**: `GET`
* **URL**: `/api/recipients/{recipient_id}`
* **Purpose**: Retrieve a single recipient by its UUID.

#### Response (`200 OK`)
```json
{
  "id": "d74b5cd9-6226-4f38-be6c-56590fb49477",
  "name": "EduTech NGO",
  "recipient_type": "NGO",
  "location": "New York, NY",
  "required_device_type": "Laptop",
  "minimum_ram": "8GB",
  "minimum_storage": "256GB",
  "quantity_needed": 5,
  "priority": "High",
  "created_at": "2026-08-12T06:32:55",
  "updated_at": "2026-08-12T06:32:55"
}
```

#### Error Response (`404 Not Found`)
```json
{
  "detail": "Recipient with ID 'd74b5cd9-6226-4f38-be6c-56590fb49477' not found"
}
```

---

### 4.4 Delete Recipient
* **HTTP Method**: `DELETE`
* **URL**: `/api/recipients/{recipient_id}`
* **Purpose**: Delete a registered recipient by its UUID.

#### Response (`200 OK`)
```json
{
  "message": "Recipient with ID 'd74b5cd9-6226-4f38-be6c-56590fb49477' successfully deleted",
  "id": "d74b5cd9-6226-4f38-be6c-56590fb49477"
}
```

---

## 5. Database Matching API (`/api/matches/{device_id}`)

### 5.1 Get Ranked Matches for a Device
* **HTTP Method**: `GET`
* **URL**: `/api/matches/{device_id}`
* **Purpose**: Evaluate a registered device against all recipients in MySQL and return candidate recipients ranked from highest to lowest score with transparent reasons.

#### Response (`200 OK`)
```json
{
  "device_id": "b4e73869-7259-4d87-a72f-8625f72d0e7e",
  "device_type": "Laptop",
  "brand": "Dell",
  "model": "XPS 15",
  "total_candidates_evaluated": 3,
  "matches_found": 2,
  "matches": [
    {
      "recipient_id": "d74b5cd9-6226-4f38-be6c-56590fb49477",
      "recipient_name": "EduTech NGO",
      "recipient_type": "NGO",
      "location": "New York, NY",
      "match_score": 100.0,
      "matched_device_type": "Laptop",
      "type_matched": true,
      "ram_requirement": "8GB",
      "ram_result": "Satisfied: Device (16GB) >= Requirement (8GB) (+15 pts)",
      "storage_requirement": "256GB",
      "storage_result": "Satisfied: Device (512GB SSD) >= Requirement (256GB) (+15 pts)",
      "priority": "High",
      "reasons": [
        "Device type 'Laptop' matches recipient required type 'Laptop' (+50 pts)",
        "RAM: Satisfied: Device (16GB) >= Requirement (8GB) (+15 pts)",
        "Storage: Satisfied: Device (512GB SSD) >= Requirement (256GB) (+15 pts)",
        "Priority 'High' applied (+20 pts)"
      ]
    }
  ]
}
```

#### How Frontend / AI Agents Should Call This API
1. First register or select a device ID via `POST /api/devices/` or `GET /api/devices/`.
2. Issue a `GET` request to `/api/matches/{device_id}`.
3. Use the `matches` array (pre-sorted by `match_score` descending) to display recipient options or feed top recommendations into downstream logistics routing agents.

---

## 6. AI Agent Pipeline Orchestration API (`/api/matches/`)

### 6.1 Trigger AI Pipeline Matching
* **HTTP Method**: `POST`
* **URL**: `/api/matches/`
* **Purpose**: Triggers the 4-agent sequential workflow (`Object -> Condition -> Need -> Logistics`).

#### Request Body
```json
{
  "name": "Old Laptop",
  "description": "Used Dell laptop with 16GB RAM",
  "location": "Seattle, WA",
  "image_url": "https://example.com/item.jpg"
}
```
* **Required Fields**: `name`, `description`, `location`
* **Optional Fields**: `image_url`

#### Response (`200 OK`)
```json
{
  "item_name": "Old Laptop",
  "category": "Electronics",
  "condition": "Good",
  "status": "matched",
  "matches": [
    {
      "recipient": {
        "organization_id": "org-001",
        "organization_name": "Tech for All",
        "priority": "High"
      },
      "logistics": {
        "origin": "Seattle, WA",
        "destination": "Tech for All Center, Downtown",
        "distance_km": 12.5,
        "estimated_cost_usd": 15.0,
        "recommended_mode": "Ground Courier"
      },
      "score": 0.85
    }
  ]
}
```

---

## 7. Summary Matrix of All Endpoints

| Resource | HTTP Method | Endpoint | Description | Status Codes |
| :--- | :---: | :--- | :--- | :---: |
| **Devices** | `POST` | `/api/devices/` | Register new device | `201`, `500` |
| **Devices** | `GET` | `/api/devices/` | List all devices | `200`, `500` |
| **Devices** | `GET` | `/api/devices/{device_id}` | Get device details | `200`, `404` |
| **Devices** | `DELETE` | `/api/devices/{device_id}` | Remove device | `200`, `404`, `500` |
| **Recipients** | `POST` | `/api/recipients/` | Register new recipient | `201`, `500` |
| **Recipients** | `GET` | `/api/recipients/` | List all recipients | `200`, `500` |
| **Recipients** | `GET` | `/api/recipients/{recipient_id}` | Get recipient details | `200`, `404` |
| **Recipients** | `DELETE` | `/api/recipients/{recipient_id}` | Remove recipient | `200`, `404`, `500` |
| **Matching** | `GET` | `/api/matches/{device_id}` | Database-driven recipient ranking | `200`, `404`, `500` |
| **Pipeline** | `POST` | `/api/matches/` | 4-Agent AI Orchestration pipeline | `200`, `500` |
