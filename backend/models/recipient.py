from sqlalchemy import Column, String, Integer, DateTime, Text, func
import uuid
from database.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    name = Column(String(150), nullable=False, index=True)
    recipient_type = Column(String(50), nullable=False)  # e.g., NGO, School, Individual
    location = Column(String(255), nullable=False)
    required_device_type = Column(String(50), nullable=False)
    minimum_ram = Column(String(50), nullable=True)
    minimum_storage = Column(String(50), nullable=True)
    quantity_needed = Column(Integer, default=1, nullable=False)
    priority = Column(String(20), default="Medium", nullable=False)  # e.g., High, Medium, Low
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Recipient(id='{self.id}', name='{self.name}', required_device_type='{self.required_device_type}')>"
