from sqlalchemy import Column, Integer, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
class RadioTelemetryLog(Base):
    __tablename__ = "rtlogs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    base_frequency_mhz = Column(Float, nullable=False)
    noise_frequency_mhz = Column(Float, nullable=False)
    is_anomaly = Column(Boolean, nullable=False)
    harmonic_order = Column(Integer, nullable=False)
    deviation_percent = Column(Float, nullable=False)