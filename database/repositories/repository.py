from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Job, Resume, MatchResult, AuditLog, BiasReport
from sqlalchemy import UUID, select


class ResumeRepository():

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, resume: Resume):
        self.session.add(resume)
        await self.session.flush()
        return resume
    
    async def get_by_id(self, id: UUID):
        result = await self.session.get(Resume, id)
        return result if result else None
    
    async def mark_deleted(self, id: UUID):
        resume = await self.session.get(Resume, id)
        if not resume:
            raise ValueError("resume is None")
        
        resume.is_deleted = True
        await self.session.flush()

    async def list_all(self):
        result = await self.session.execute(select(Resume))
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
        return result if result else None
    
    async def list_all(self):
        result = await self.session.execute(select(Job))
        return result.scalars().all()
    
