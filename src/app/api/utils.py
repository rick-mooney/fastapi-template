from typing import Optional
from sqlalchemy import text


async def common_params(
    q: Optional[str] = None,
    page: int = 0,
    limit: int = 100,
    sort: str = "id",
    sortDir: str = "desc",
):
    return {
        "q": text(q) if q else None,
        "page": page * limit,
        "limit": limit,
        "sort_by": text(" ".join([sort, sortDir])),
    }


def copy_attributes(source, destination):
    """
    Copies attributes from `source` object to `destination` object if they exist in both objects
    """
    for var, value in vars(source).items():
        if hasattr(destination, var):
            setattr(destination, var, value)
