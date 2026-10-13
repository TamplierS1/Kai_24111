import secrets
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

ASYNC_DB_URL = "sqlite+aiosqlite:///./links.db"
engine = create_async_engine(ASYNC_DB_URL, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    original: Mapped[str] = mapped_column(
        String,
    )
    short: Mapped[str] = mapped_column(String, unique=True)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


class LinkCreate(BaseModel):
    original: str


class LinkResponse(LinkCreate):
    id: int
    short: str
    model_config = ConfigDict(from_attributes=True)


@app.post("/links", response_model=LinkResponse)
async def create_link(link: LinkCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    short_link = "http://127.0.0.1:8000/" + secrets.token_urlsafe(6)

    db_link = Link(original=link.original, short=short_link)
    db.add(db_link)
    await db.commit()
    await db.refresh(db_link)

    return db_link


@app.get("/links", response_model=list[LinkResponse])
async def get_all_links(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Link))
    return result.scalars().all()


@app.get("/links/{short_link}")
async def open_short_link(
    short_link: str, db: Annotated[AsyncSession, Depends(get_db)]
):
    short_link = "http://127.0.0.1:8000/" + short_link

    result = await db.execute(select(Link).where(Link.short == short_link))
    db_link = result.scalars().first()

    if db_link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link with url {short_link} was not found",
        )

    return RedirectResponse(db_link.original)
