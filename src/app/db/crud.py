from sqlalchemy import func
from app.db.models import User
from app.config import Scopes

def set_audit_fields(record, user_id):
    record.created_by_id = record.created_by_id if record.created_by_id else user_id
    record.modified_by_id = user_id
    return record


def get_user_by_email(db, email: str) -> User:
    return db.query(User).filter(func.lower(User.email) == func.lower(email)).first()


def save_resource(db, record, user_id: int):
    record = set_audit_fields(record, user_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_resource(db, existing, updated, user_id: int):
    for var, value in updated.items():
        setattr(existing, var, value)
    return save_resource(db, existing, user_id)


def save_resource_bulk(db, resource, data, user_id: int):
    d = []
    for row in data:
        row = set_audit_fields(row, user_id)
        d.append(row.__dict__)
    db.bulk_update_mappings(resource, d)
    db.commit()


def list_resource(db, resource, params, user):
    limit = params["limit"]
    offset = params["page"]
    sort_by = params["sort_by"]
    query_filter = params["q"]
    if Scopes.ADMIN in user.scopes:
        if query_filter is not None:
            total_records = db.query(resource.id).filter(query_filter).count()
            return (
                db.query(resource)
                .filter(query_filter)
                .filter_by(is_deleted=False)
                .order_by(sort_by)
                .offset(offset)
                .limit(limit)
                .all()
            ), total_records
        else:
            total_records = db.query(resource.id).count()
            return (
                db.query(resource)
                .filter_by(is_deleted=False)
                .order_by(sort_by)
                .offset(offset)
                .limit(limit)
                .all()
            ), total_records
    else:
        if query_filter is not None:
            total_records = db.query(resource.id).filter(query_filter).filter_by(created_by_id=user.id).count()
            return (
                db.query(resource)
                .filter(query_filter)
                .filter_by(is_deleted=False)
                .filter_by(created_by_id=user.id)
                .order_by(sort_by)
                .offset(offset)
                .limit(limit)
                .all()
            ), total_records
        else:
            total_records = db.query(resource.id).filter_by(created_by_id=user.id).count()
            return (
                db.query(resource)
                .filter_by(is_deleted=False)
                .filter_by(created_by_id=user.id)
                .order_by(sort_by)
                .offset(offset)
                .limit(limit)
                .all()
            ), total_records


def list_resource_all(db, resource):
    return db.query(resource).filter_by(is_deleted=False).order_by(resource.id.desc()).all()


def query_by_external_id(db, resource, external_id, u):
    if Scopes.ADMIN in u.scopes:
        return (
            db.query(resource)
            .filter_by(external_id=external_id)
            .filter_by(is_deleted=False)
            .first()
        )
    else:
        return (
            db.query(resource)
            .filter_by(external_id=external_id)
            .filter_by(is_deleted=False)
            .filter_by(created_by_id=u.id)
            .first()
        )   


def delete(db, resource, user_id: int):
    resource.is_deleted = True
    save_resource(db, resource, user_id)
