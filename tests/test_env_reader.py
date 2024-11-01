"""このモジュールは環境変数の取得とテストを行います。"""

import pytest

from src.utils.env_reader import EnvVariableNotFoundError, get_env_value


def test_get_env_value(monkeypatch):
    # 環境変数をモック
    monkeypatch.setenv("TEST_KEY", "test_value")

    # 正常なキーのテスト
    assert get_env_value("TEST_KEY") == "test_value"

    # 存在しないキーのテスト
    with pytest.raises(EnvVariableNotFoundError):
        get_env_value("NON_EXISTENT_KEY")
