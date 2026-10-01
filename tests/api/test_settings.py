from order_api.postgres_repository import PostgresPromoCodeRepository
from order_api.promo_repository import InMemoryPromoCodeRepository
from order_api.settings import promo_repository_from_env


def test_without_database_url_promo_codes_are_in_memory(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert isinstance(promo_repository_from_env(), InMemoryPromoCodeRepository)


def test_empty_database_url_means_in_memory(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "")
    assert isinstance(promo_repository_from_env(), InMemoryPromoCodeRepository)


def test_database_url_selects_postgres_without_connecting(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db:5432/orders")
    assert isinstance(promo_repository_from_env(), PostgresPromoCodeRepository)
