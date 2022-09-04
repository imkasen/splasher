import json
import random
import string
from pathlib import Path
from typing import Any

import pytest

from splasher.config.args import SETTINGS
from splasher.config.settings.settings_creator import create_settings


def random_str(length: int = random.randint(5, 10)) -> str:
    """
    Randomly generate a string which contains 5-10 characters.
    :return: random string name
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.mark.order(before="settings_arg_getter_test.py::test_get_settings_arg")
def test_create_settings(tmp_path: Path) -> None:
    """
    Test function "create_settings".
    Execute the function to create a new temporary setting file,
    check whether the new file exists,
    check whether the content is the same with "SETTINGS".
    """
    tmp_file: Path = tmp_path / f"{random_str()}.json"
    create_settings(str(tmp_file.resolve()))
    settings_dict: Any = json.loads(tmp_file.read_text())
    # assert
    assert tmp_file.is_file() is True
    assert settings_dict == SETTINGS
    # clean
    tmp_file.unlink()
