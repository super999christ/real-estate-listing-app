def bulk_query_to_dict(results) -> list[dict[str, str]]:
    """
    Function for transforming rows of a SQLAlchemy model
    into an iterpretable python list of dictionaries.
    """
    return [{column.name: str(getattr(row, column.name)) for column in row.__table__.columns} for row in results]
