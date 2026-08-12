from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.models.recipient import Recipient

router = APIRouter(prefix="/recipients", tags=["recipients"])

class RecipientCreate(BaseModel):
    name: str = Field(..., description="Name of recipient or organization")
    recipient_type: str = Field(..., description="Type of recipient (e.g. NGO, School, Individual)")
    location: str = Field(..., description="Physical location or city/region")
    required_device_type: str = Field(..., description="Required device category (e.g. Laptop, Smartphone)")
    minimum_ram: Optional[str] = Field(None, description="Minimum RAM requirement (e.g. 8GB)")
    minimum_storage: Optional[str] = Field(None, description="Minimum storage requirement (e.g. 256GB)")
    quantity_needed: int = Field(1, ge=1, description="Quantity of devices needed")
    priority: str = Field("Medium", description="Priority level (High, Medium, Low)")

class RecipientResponse(BaseModel):
    id: str
    name: str
    recipient_type: str
    location: str
    required_device_type: str
    minimum_ram: Optional[str] = None
    minimum_storage: Optional[str] = None
    quantity_needed: int
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=RecipientResponse, status_code=status.HTTP_201_CREATED)
def create_recipient(recipient_in: RecipientCreate, db: Session = Depends(get_db)):
    """
    Register a new recipient organization or individual.
    Generates a unique UUID and saves to MySQL database.
    """
    try:
        new_recipient = Recipient(
            name=recipient_in.name,
            recipient_type=recipient_in.recipient_type,
            location=recipient_in.location,
            required_device_type=recipient_in.required_device_type,
            minimum_ram=recipient_in.minimum_ram,
            minimum_storage=recipient_in.minimum_storage,
            quantity_needed=recipient_in.quantity_needed,
            priority=recipient_in.priority
        )
        db.add(new_recipient)
        db.commit()
        db.refresh(new_recipient)
        return new_recipient
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create recipient: {str(e)}"
        )

@router.get("/", response_model=List[RecipientResponse])
def get_recipients(db: Session = Depends(get_db)):
    """
    Retrieve all registered recipients.
    """
    try:
        recipients = db.query(Recipient).all()
        return recipients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while retrieving recipients: {str(e)}"
        )

@router.get("/{recipient_id}", response_model=RecipientResponse)
def get_recipient_by_id(recipient_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a recipient by its unique UUID.
    Returns HTTP 404 if recipient is not found.
    """
    recipient = db.query(Recipient).filter(Recipient.id == recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipient with ID '{recipient_id}' not found"
        )
    return recipient

@router.delete("/{recipient_id}", status_code=status.HTTP_200_OK)
def delete_recipient(recipient_id: str, db: Session = Depends(get_db)):
    """
    Delete a recipient by its unique UUID.
    Returns HTTP 404 if recipient is not found.
    """
    recipient = db.query(Recipient).filter(Recipient.id == recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipient with ID '{recipient_id}' not found"
        )
    try:
        db.delete(recipient)
        db.commit()
        return {
            "message": f"Recipient with ID '{recipient_id}' successfully deleted",
            "id": recipient_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete recipient: {str(e)}"
        )
