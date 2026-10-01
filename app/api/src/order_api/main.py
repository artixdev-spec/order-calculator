"""FastAPI-приложение. Логика расчёта — в пакете ``order_core``."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from order_api.promo_repository import PromoCodeRepository
from order_api.schemas import ErrorOut, OrderIn, PromoCodeOut, ReceiptOut
from order_api.settings import promo_repository_from_env
from order_core import OrderError, calculate_receipt


def create_app(promo_codes: PromoCodeRepository | None = None) -> FastAPI:
    """Собрать приложение. Без явного хранилища — выбор по ``DATABASE_URL``."""
    repository = promo_codes if promo_codes is not None else promo_repository_from_env()
    app = FastAPI(title="Order calculator", version="0.1.0")

    @app.exception_handler(OrderError)
    def order_error_handler(request: Request, error: OrderError) -> JSONResponse:
        body = ErrorOut(error=type(error).__name__, detail=str(error))
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/promo-codes")
    def list_promo_codes() -> list[PromoCodeOut]:
        return [PromoCodeOut.from_domain(p) for p in repository.all().values()]

    @app.post("/quote", responses={422: {"model": ErrorOut}})
    def quote(order: OrderIn) -> ReceiptOut:
        """Рассчитать стоимость заказа: скидки, промокод, доставка."""
        receipt = calculate_receipt(order.to_domain(), repository.all())
        return ReceiptOut.from_domain(receipt)

    return app


app = create_app()
