from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from sqlalchemy import Column, Enum, Integer, Float, String, TEXT, Boolean, JSON, DateTime, ForeignKey
from uuid import uuid4

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(Enum("pdf", "docx"), nullable=False)
    file_path = Column(String, nullable=False)
    raw_text = Column(TEXT, nullable=False)
    cleaned_text = Column(TEXT, nullable=False)
    language = Column(String, nullable=False)
    pii_scrubbed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    is_deleted = Column(Boolean, default=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    title = Column(String, nullable=False)
    raw_text = Column(TEXT, nullable=False)
    parsed_requirements = Column(JSON, nullable=False)
    seniority = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True) 
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class BiasReport(Base):
    __tablename__ = "bias_reports"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    group_name = Column(String, nullable=False)
    passed_threshold = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    shap_values = Column(JSON, nullable=False)
    top_features = Column(JSON, nullable=False)
    explanation = Column(TEXT, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
