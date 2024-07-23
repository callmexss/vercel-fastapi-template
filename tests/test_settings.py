from pathlib import Path

from app.config import settings


def test_settings_path_correct():
    assert settings.ROOT_PATH == Path(__file__).parent.parent
    assert settings.STATIC_PATH.exists() and settings.STATIC_PATH.name == "static"
