from core.repositories import category_repo


def get_all_categories(session):
    return category_repo.get_all_categories(session)


def create_category(session, name: str):

    name = name.strip()

    if not name:
        raise ValueError("Название категории пустое")

    existing = category_repo.get_category_by_name(
        session,
        name
    )

    if existing:
        raise ValueError("Категория уже существует")

    return category_repo.create_category(
        session,
        name
    )


def delete_category(session, category_id: int):

    category = category_repo.get_category_by_id(
        session,
        category_id
    )

    if not category:
        raise ValueError(
            "Категория не найдена"
        )

    category_repo.delete_category(
        session,
        category
    )


def rename_category(
    session,
    category_id: int,
    new_name: str
):

    category = category_repo.get_category_by_id(
        session,
        category_id
    )

    if not category:
        raise ValueError(
            "Категория не найдена"
        )

    existing = category_repo.get_category_by_name(
        session,
        new_name
    )

    if existing and existing.id != category.id:
        raise ValueError(
            "Категория уже существует"
        )

    category_repo.rename_category(
        session,
        category,
        new_name
    )
