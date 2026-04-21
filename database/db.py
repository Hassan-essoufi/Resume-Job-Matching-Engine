from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from config.settings import get_settings
from database.models import Base

SETTINGS = get_settings()
DB_URL = SETTINGS.database.url
SYNC_DB_URL = SETTINGS.database.url_sync

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine,
                            class_=AsyncSession,
                            expire_on_commit=False)

sync_engine = create_engine(SYNC_DB_URL, echo=True)

async def get_async_session():
    async with AsyncSessionLocal() as session:
            yield session
    
def create_all_tables():
    Base.metadata.create_all(sync_engine)