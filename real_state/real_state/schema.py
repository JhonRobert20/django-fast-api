from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


def confirm_coordinate(value: str) -> str:
    """
    Validation to prevent corrupted coordinates field.
    Called by the helper function below;
    """
    if value:
        error = False
        coordinate = value.split(",")
        if len(coordinate) != 2:
            error = True
        else:
            try:
                float(coordinate[0])
                float(coordinate[1])
            except ValueError:
                error = True
        if error:
            raise ValueError("Coordinates must be in the format of 'lat,lng'.")

    return value


class EstateBase(BaseModel):
    build_status: Optional[str] = ""
    is_active: Optional[bool] = True
    start_month: Optional[int] = 0
    construction_type: Optional[int] = None
    date_diff: Optional[int] = None
    description: Optional[str] = ""
    date_in: Optional[datetime] = None
    property_type: Optional[int] = None
    end_week: Optional[int] = None
    typology_type: Optional[int] = None
    id: str
    coordinates: Optional[str] = None
    boundary_id: Optional[str] = None
    id_uda: Optional[str] = ""
    title: Optional[str] = None
    listing_type: Optional[int] = None
    date: Optional[datetime] = None

    _check_coordinate = validator("coordinates", allow_reuse=True)(confirm_coordinate)


class OrderBy(BaseModel):
    field: Optional[str] = None
    direction: Optional[str] = None


class PaginatedEstates(BaseModel):
    objects: Optional[List[EstateBase]] = None
    page: Optional[int] = 0
    pages: Optional[int] = 0
    has_next: Optional[bool] = False
    has_prev: Optional[bool] = False
    order_by: Optional[OrderBy] = None
    total_results: Optional[int] = 0
