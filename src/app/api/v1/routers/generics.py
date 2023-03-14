import inspect
from fastapi import APIRouter, Depends, Security, Request
from app.db.session import SessionManager
from app.api.utils import common_params
from app.db.crud import (
    save_resource, update_resource, list_resource, query_by_external_id, delete
)
from app.api.auth import get_current_active_user
from app.api.schemas import ListResource, UserOut
from app.config import Scopes
import app.db.models as models
from app.exceptions import Codes

router = APIRouter(prefix=f"/api/v1")


async def get_request_body(request: Request, model):
    req = await request.json()
    return model(**req)


def get_resource_model(resource: str):
    resource_dict = {r[0]: r[1] for r in inspect.getmembers(models, inspect.isclass)}
    if resource.title() in resource_dict:
        return resource_dict.get(resource.title())
    else:
        raise Codes.NOT_FOUND


@router.get("/{resource}")
async def list_records(
    resource: str,
    commons=Depends(common_params),
    u: UserOut = Security(get_current_active_user, scopes=[Scopes.USER]),
):
    with SessionManager() as db:
        model = get_resource_model(resource)
        results, total = list_resource(db, model, commons, u)
        return ListResource(data=results, total=total)


@router.get("/{resource}/{recordid}")
async def get_record(
    resource: str,
    recordid: str,
    u: UserOut = Security(get_current_active_user, scopes=[Scopes.USER]),
):
    model = get_resource_model(resource)
    with SessionManager() as db:
        record = query_by_external_id(db, model, recordid, u)
        if not record:
            raise Codes.NOT_FOUND
        return record


@router.post("/{resource}")
async def create_record(
    resource: str,
    request: Request,
    u: UserOut = Security(get_current_active_user, scopes=[Scopes.USER]),
):
    model = get_resource_model(resource)
    data = await get_request_body(request, model)
    with SessionManager() as db:
        record = save_resource(db, data, u.id)
        return record


@router.put("/{resource}/{recordid}")
async def update_record(
    resource: str,
    recordid: str,
    request: Request,
    u: UserOut = Security(get_current_active_user, scopes=[Scopes.USER]),
):
    model = get_resource_model(resource)
    with SessionManager() as db:
        existing_record = query_by_external_id(db, model, recordid, u)
        if not existing_record:
            raise Codes.NOT_FOUND
        data = await request.json()
        record = update_resource(db, existing_record, data, u.id)
        return record


@router.delete("/{resource}/{recordid}")
async def delete_record(
    resource: str,
    recordid: str,
    u: UserOut = Security(get_current_active_user, scopes=[Scopes.USER]),
):
    model = get_resource_model(resource)
    with SessionManager() as db:
        record = query_by_external_id(db, model, recordid, u)
        if not record:
            return Codes.NOT_FOUND
        delete(db, record, u.id)
        return
