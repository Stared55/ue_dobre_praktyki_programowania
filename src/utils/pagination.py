from fastapi import Query
from typing import Tuple

def pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
) -> Tuple[int, int]:
    return skip, limit

