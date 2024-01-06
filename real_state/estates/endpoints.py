from typing import Any, Optional

from fastapi import APIRouter, Depends

from real_state.auth import is_logged
from real_state.mongodb import get_paginator_mongo, mongodb
from real_state.schema import EstateBase, PaginatedEstates

router = APIRouter()


@router.get("/estates/", response_model=PaginatedEstates)
def get_all(
    page: int = 1,
    page_size: int = 10,
    is_active: bool = False,
    logged: bool = Depends(is_logged),
) -> PaginatedEstates:
    """
    Get all estates - paginated
    """

    order_by = [{"field": "date", "ordering": "ASC"}]

    filter_states = {"is_active": is_active}

    return get_paginator_mongo(
        mongodb.estates_collection,
        filter_states,
        page_size,
        page,
        PaginatedEstates,
        order_by=order_by,
    )


@router.post("/estates/", response_model=EstateBase)
def create_or_update_estate(
    estate: EstateBase, logged: bool = Depends(is_logged)
) -> EstateBase:
    """
    Create a real state.
    """
    estate = estate.dict()
    mongodb.update_many_estates([estate])
    return list(mongodb.filter_estates({"_id": str(estate["id"])}))[0]


@router.get("/estates/{estate_id}", response_model=Optional[EstateBase])
def get_estate(estate_id: str, logged: bool = Depends(is_logged)) -> Any:
    """
    Get a real state based on its id.
    """
    filtered = list(mongodb.filter_estates({"_id": estate_id}))

    return filtered[0] if filtered else None
