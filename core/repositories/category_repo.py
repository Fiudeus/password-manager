from sqlalchemy import select
from core.models import Category


def create_category(session, name: str) -> Category:
    category = Category(name=name)
    session.add(category)
    session.flush()
    return category


def get_category_by_name(session, name: str) -> Category | None:
    stmt = select(Category).where(Category.name == name)
    return session.execute(stmt).scalars().first()


def get_category_by_id(session, category_id: int) -> Category | None:
    stmt = select(Category).where(Category.id == category_id)
    return session.execute(stmt).scalars().first()


def get_all_categories(session) -> list[Category]:
    stmt = select(Category)
    return session.execute(stmt).scalars().all()


def delete_category(session, category: Category) -> None:
    session.delete(category)
    session.flush()