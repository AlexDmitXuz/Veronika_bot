import asyncpg
from typing import Optional, List, Any
from aiogram.types import User  # Используется в register_client
from config import load_config

pool: Optional[asyncpg.pool.Pool] = None

config = load_config()

pool = None

async def create_pool():
    global pool
    pool = await asyncpg.create_pool(dsn=config.db)
    return pool

# Добавление новой фотосессии
async def add_photo_session(user_id: int, username: str, session_type: str, session_date: str, session_time: str):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO photo_sessions (user_id, username, session_type, session_date, session_time)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_id, username, session_type, session_date, session_time
        )

# Получение всех сессий
async def get_all_sessions() -> List[asyncpg.Record]:
    async with pool.acquire() as conn:
        return await conn.fetch(
            "SELECT * FROM photo_sessions ORDER BY session_date, session_time"
        )

# Обновление конкретного поля в фотосессии
async def update_session_field(session_id: int, field: str, value: Any):
    allowed_fields = {"session_type", "session_date", "session_time", "status", "contact_phone"}
    if field not in allowed_fields:
        raise ValueError(f"Недопустимое поле для обновления: {field}")

    query = f"UPDATE photo_sessions SET {field} = $1 WHERE id = $2"
    async with pool.acquire() as conn:
        await conn.execute(query, value, session_id)

# Регистрация клиента (если ещё не зарегистрирован)
async def register_client(user: User):
    query = """
    INSERT INTO clients (user_id, username, first_name, last_name, language_code, is_bot)
    VALUES ($1, $2, $3, $4, $5, $6)
    ON CONFLICT (user_id) DO NOTHING
    """
    async with pool.acquire() as conn:
        await conn.execute(query,
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code,
            user.is_bot
        )

# Архивация завершённых или отменённых сессий
async def archive_old_sessions():
    query_copy = """
    INSERT INTO archive_sessions (user_id, username, session_type, session_date, session_time, status)
    SELECT user_id, username, session_type, session_date, session_time, status
    FROM photo_sessions
    WHERE status IN ('status_cancelled', 'status_completed')
    """
    query_delete = """
    DELETE FROM photo_sessions
    WHERE status IN ('status_cancelled', 'status_completed')
    """
    async with pool.acquire() as conn:
        await conn.execute(query_copy)
        await conn.execute(query_delete)
