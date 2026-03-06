from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, RedirectResponse

from ..core.schemas import SuccessResponse
from ..config import settings

router = APIRouter()


@router.get(
    '/',
    summary=(
        'Ресурс для редиректа на Swagger документацию при переходе на '
        'эндпоинт api/v1/'
    ),
    include_in_schema=False
)
def index() -> RedirectResponse:
    swagger_url = f'{settings.api_url}/docs'
    return RedirectResponse(url=swagger_url)


@router.get(
    '/healthcheck',
    summary='Проверка состояния работоспособности сервиса',
)
def healthcheck(
) -> SuccessResponse:
    return SuccessResponse(
        message='Сервис в рабочем состоянии'
    )
