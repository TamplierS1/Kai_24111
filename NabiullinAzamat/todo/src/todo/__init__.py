from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

ASYNC_DB_URL = "sqlite+aiosqlite:///./tasks.db"
engine = create_async_engine(ASYNC_DB_URL, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String,
    )
    description: Mapped[str] = mapped_column(String, unique=True)
    is_completed: Mapped[bool] = mapped_column(default=False)


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


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskResponse(TaskCreate):
    id: int
    title: str
    description: str
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    db_task = Task(title=task.title, description=task.description, is_completed=False)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    return db_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalars().first()

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found",
        )

    await db.delete(db_task)
    await db.commit()

    return status.HTTP_204_NO_CONTENT


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def complete_task(task_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalars().first()

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found",
        )

    db_task.is_completed = True
    await db.commit()
    await db.refresh(db_task)

    return db_task


@app.get("/tasks", response_model=list[TaskResponse])
async def get_all_tasks(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Task))
    return result.scalars().all()
