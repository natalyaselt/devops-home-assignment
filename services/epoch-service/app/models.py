from pydantic import BaseModel
from datetime import datetime


class EpochRequest(BaseModel):
    """
    Request model for /epoch endpoint.
    """

    date: datetime


class EpochResponse(BaseModel):
    """
    Response model for /epoch endpoint.
    """

    epoch: int
