import argparse
from app.api.schemas import UserOut
from app.db.models import User
from app.db.session import SessionManager


def handle(*args):
    parser = argparse.ArgumentParser(
        description="Example of creating a script with fast api"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=True,
        help="Example of a required parameter.  Select a model to query",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="Limit the number of records to return",
    )
    parser.add_argument("--dry_run", action="store_true")
    params = parser.parse_args(*args)
    print(params.model)
    print(params.limit)
    print(params.dry_run)
    with SessionManager() as db:
        return db.query(User).limit(params.limit).count()