from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

DATABASE_URL = "sqlite:///./codewatch.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    total_issues = Column(Integer, default=0)
    pylint_count = Column(Integer, default=0)
    bandit_count = Column(Integer, default=0)
    semgrep_count = Column(Integer, default=0)
    sast_results = Column(Text)   # JSON string
    llm_report = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_analysis(filename, sast_results, llm_report):
    db = SessionLocal()
    summary = sast_results.get("summary", {})
    record = Analysis(
        filename=filename,
        total_issues=sast_results.get("total_issues", 0),
        pylint_count=summary.get("pylint_count", 0),
        bandit_count=summary.get("bandit_count", 0),
        semgrep_count=summary.get("semgrep_count", 0),
        sast_results=json.dumps(sast_results),
        llm_report=llm_report
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return record.id

def get_all_analyses():
    db = SessionLocal()
    records = db.query(Analysis).order_by(Analysis.created_at.desc()).limit(20).all()
    db.close()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "total_issues": r.total_issues,
            "pylint_count": r.pylint_count,
            "bandit_count": r.bandit_count,
            "semgrep_count": r.semgrep_count,
            "sast_results": json.loads(r.sast_results),
            "llm_report": r.llm_report,
            "created_at": r.created_at.strftime("%d/%m %H:%M")
        }
        for r in records
    ]
