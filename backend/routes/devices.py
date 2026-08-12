from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.models.device import Device

router = APIRouter(prefix="/devices", tags=["devices"])

class DeviceCreate(BaseModel):
    device_type: str = Field(..., description="Type of electronic device (e.g. Laptop, Smartphone, Tablet)")
    brand: Optional[str] = Field(None, description="Manufacturer/Brand name")
    model: Optional[str] = Field(None, description="Device model name/number")
    year: Optional[int] = Field(None, description="Manufacturing or release year")
    ram: Optional[str] = Field(None, description="RAM capacity (e.g. 8GB, 16GB)")
    storage: Optional[str] = Field(None, description="Storage capacity (e.g. 256GB SSD, 1TB)")
    owner_info: Optional[str] = Field(None, description="Information about owner or donor")

class DeviceResponse(BaseModel):
    id: str
    device_type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    owner_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db)):
    """
    Register a new electronic device.
    Generates a unique UUID and persists to MySQL database.
    """
    try:
        new_device = Device(
            device_type=device_in.device_type,
            brand=device_in.brand,
            model=device_in.model,
            year=device_in.year,
            ram=device_in.ram,
            storage=device_in.storage,
            owner_info=device_in.owner_info
        )
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create device: {str(e)}"
        )

@router.get("/", response_model=List[DeviceResponse])
def get_devices(db: Session = Depends(get_db)):
    """
    Retrieve all registered electronic devices.
    """
    try:
        devices = db.query(Device).all()
        return devices
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while retrieving devices: {str(e)}"
        )

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single device by its unique ID.
    Returns HTTP 404 if device is not found.
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID '{device_id}' not found"
        )
    return device

@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
def delete_device(device_id: str, db: Session = Depends(get_db)):
    """
    Delete a registered device by its unique ID.
    Returns HTTP 404 if device is not found.
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID '{device_id}' not found"
        )
    try:
        db.delete(device)
        db.commit()
        return {
            "message": f"Device with ID '{device_id}' successfully deleted",
            "id": device_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete device: {str(e)}"
        )
