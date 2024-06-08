from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Config


# get the database url from config file
DB_URL = Config.DB_URL

# initialize the database, its Base `class`, and its SessionLocal `class`
Base = declarative_base()


async def transaction(msg: str | None) -> dict[str, str]:
    """
    boiler-plate transaction function, used in every `CRUD`
    operation after inserting/updating/deleting records.
    """
    try:
        await db.commit()
        return {'TransactionSuccess': msg}
    except Exception:
        await db.rollback()
        return {'TransactionError': 'Something went wrong / Reverting changes'}


class AsyncDatabaseSession:
    """class for handling/creating asynchronous database session"""
    def __init__(self):
        self.engine = create_async_engine(
            DB_URL,
            future=True,
            echo=False,  # turned off logging; set to True if you can't identify a problem
        )
        self.session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )()

    def __getattr__(self, name):
        return getattr(self.session, name)

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# the main database variable used for all operations
db = AsyncDatabaseSession()
