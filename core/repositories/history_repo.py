from sqlalchemy import select
from core.models import PasswordHistory


def create_history(session, password_id: int, old_password: str) -> PasswordHistory:
    history = PasswordHistory(
        password_id=password_id,
        old_password=old_password
    )
    session.add(history)
    session.flush()
    return history


def get_history_by_password_id(session, password_id: int) -> list[PasswordHistory]:
    stmt = (
        select(PasswordHistory)
        .where(PasswordHistory.password_id == password_id)
        .order_by(PasswordHistory.changed_at.desc())
    )
    return session.execute(stmt).scalars().all()


def get_history_entry(session, history_id: int) -> PasswordHistory | None:
    stmt = select(PasswordHistory).where(PasswordHistory.id == history_id)
    return session.execute(stmt).scalars().first()


def delete_history(session, history: PasswordHistory) -> None:
    session.delete(history)
    session.flush()


def clear_history_for_password(session, password_id: int) -> None:
    stmt = select(PasswordHistory).where(PasswordHistory.password_id == password_id)
    history_items = session.execute(stmt).scalars().all()

    for item in history_items:
        session.delete(item)

    session.flush()