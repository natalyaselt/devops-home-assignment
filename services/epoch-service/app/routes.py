from fastapi import APIRouter
from app.models import EpochRequest, EpochResponse
from app.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/epoch",
    response_model=EpochResponse,
    summary="Convert ISO-8601 date to Unix epoch",
)
def get_epoch(request: EpochRequest) -> EpochResponse:
    """
    Convert ISO-8601 datetime to Unix epoch timestamp.

    Request example:
        {
            "date": "2026-06-15T10:00:00Z"
        }

    Response example:
        {
            "epoch": 1781517600
        }

    Returns:
        EpochResponse containing epoch seconds.
    """
    logger.info("Received request for date: %s", request.date)

    epoch = int(request.date.timestamp())

    logger.info("Returning epoch: %d", epoch)

    return EpochResponse(epoch=epoch)
