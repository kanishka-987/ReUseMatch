from sqlalchemy import Column, String, Integer, DateTime, Text, func
import uuid
from database.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class Device(Base):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    device_type = Column(String(50), nullable=False, index=True)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    ram = Column(String(50), nullable=True)
    storage = Column(String(50), nullable=True)
    owner_info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Device(id='{self.id}', device_type='{self.device_type}', brand='{self.brand}', model='{self.model}')>"
