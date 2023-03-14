import typing as t


T = t.TypeVar("T")


def seed_table(model: T, data: t.List[t.Any], db_connection):
    for d in data:
        record = model(**d)
        db_connection.add(record)
    db_connection.commit()

# Add database metadata as JSON here
