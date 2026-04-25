from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Job, Resume, MatchResult, AuditLog, BiasReport
from sqlalchemy import select
from uuid import UUID

class ResumeRepository():

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, resume: Resume):
        self.session.add(resume)
        await self.session.flush()
        return resume
    
    async def get_by_id(self, id: UUID):
        result = await self.session.get(Resume, id)
        return result
    
    async def mark_deleted(self, id: UUID):
        resume = await self.session.get(Resume, id)
        if not resume:
            raise ValueError("resume is None")
        
        resume.is_deleted = True
        await self.session.flush()

    async def list_all(self, limit: int, offset: int):
        result = await self.session.execute(select(Resume).where(Resume.is_deleted == False).limit(limit).offset(offset))
        return result.scalars().all()

class JobRepository():

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, job: Job):
        self.session.add(job)
        await self.session.flush()
        return job
    
    async def get_by_id(self, id: UUID):
        result = await self.session.get(Job, id)
        return result 
    
    async def list_all(self, limit: int, offset: int):
        result = await self.session.execute(select(Job).order_by(Job.created_at.desc()).limit(limit).offset(offset))
        return result.scalars().all()


class MatchRepository():

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, match_result: MatchResult):
        self.session.add(match_result)
        await self.session.flush()
        return match_result
    
    async def get_by_resume(self, resume_id: UUID):
        result = await self.session.execute(select(MatchResult).where(MatchResult.resume_id == resume_id).order_by(MatchResult.score.desc()))
        return result.scalars().all()
    
    async def get_by_job(self, job_id: UUID):
        result = await self.session.execute(select(MatchResult).where(MatchResult.job_id == job_id))
        return result.scalars().all()
    
    async def get_top_for_job(self, job_id: UUID, top_k: int):
        result = await self.session.execute(select(MatchResult).where(MatchResult.job_id == job_id).order_by(MatchResult.score.desc()).limit(top_k))
        return result.scalars().all()
    

class AuditRepository():
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, log: AuditLog):
        self.session.add(log)
        await self.session.flush()
        return log
    
    async def get_trail_by_resume(self, resume_id:  UUID):
        result = await self.session.execute(select(AuditLog).where(AuditLog.resume_id == resume_id).order_by(AuditLog.created_at.asc()))
        return result.scalars().all()
    
class BiasRepository():

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_report(self, report: BiasReport):
        self.session.add(report)
        await self.session.flush()
        return report 
    
    async def get_by_job(self, job_id: UUID):
        result = await self.session.execute(select(BiasReport).where(BiasReport.job_id == job_id).order_by(BiasReport.created_at.desc()))
        return result.scalars().all()
    
    async def get_failed(self, job_id: UUID):
        result = await self.session.execute(select(BiasReport).where(BiasReport.job_id == job_id, BiasReport.passed_threshold == False))
        return result.scalars().all()
    


    
