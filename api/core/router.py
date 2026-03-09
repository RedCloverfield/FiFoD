from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ..core.schemas import SuccessResponse
from ..config import settings

router = APIRouter()


@router.get(
    '/',
    summary=(
        'Ресурс для редиректа на Swagger документацию при переходе на '
        'эндпоинт /'
    ),
    include_in_schema=False
)
def index() -> RedirectResponse:
    swagger_url = f'{settings.api_url}/docs'
    return RedirectResponse(url=swagger_url)


@router.get(
    '/healthcheck',
    summary='Ресурс для проверки состояния работоспособности сервиса',
)
def healthcheck(
) -> SuccessResponse:
    return SuccessResponse(
        message='Сервис в рабочем состоянии'
    )
