import pytest

from app.core.config import Settings, get_settings


def test_settings_load():
    settings = get_settings()
    assert settings.APP_NAME == "MEDORA AI"
    assert settings.is_development is True


def test_env_validation():
    prod = Settings(APP_ENV="production")
    assert prod.APP_ENV == "production"
    assert prod.is_development is False
    assert prod.is_production is True

    with pytest.raises(ValueError):
        Settings(APP_ENV="invalid_environment")
