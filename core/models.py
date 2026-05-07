from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import relationship
from core.database import Base


# Здесь находятся модели баз данных (структура таблиц SQLAlchemy)


# Таблица пользователей

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    master_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    passwords = relationship("Password", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"

# Таблица паролей

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    site = Column(String, nullable=False)
    login = Column(String, nullable=True)
    password = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="passwords")
    history = relationship(
        "PasswordHistory", back_populates="password",
        order_by="PasswordHistory.changed_at.desc()", cascade="all, delete-orphan"
    )
    categories = relationship("Category", secondary="category_passwords", back_populates="passwords")


    def __repr__(self):
        return f"Password(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at} password=********, user_id={self.user_id})"

Index("idx_passwords_user_id", Password.user_id)

# Таблица истории паролей

class PasswordHistory(Base):
    __tablename__ = "password_history"

    id = Column(Integer, primary_key=True)
    password_id = Column(Integer, ForeignKey("passwords.id"), nullable=False)
    old_password = Column(String, nullable=False)
    changed_at = Column(DateTime, server_default=func.now())

    password = relationship("Password", back_populates="history")

    def __repr__(self):
        return f"PasswordHistory(id={self.id}, password_id={self.password_id}, old_password={self.old_password}, changed_at={self.changed_at})"

# Таблица категорий

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    passwords = relationship("Password", secondary="category_passwords", back_populates="categories")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"

# Таблица, связывающая категории и пароли

class CategoryPassword(Base):
    __tablename__ = "category_passwords"
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    password_id = Column(Integer, ForeignKey("passwords.id"), primary_key=True)

    def __repr__(self):
        return f"CategoryPassword(category_id={self.category_id}, password_id={self.password_id})"