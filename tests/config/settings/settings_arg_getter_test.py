import json
import random
import string
from pathlib import Path

import pytest

from splasher.config.settings import get_settings_arg


def random_str(length: int = random.randint(5, 10)) -> str:
    """
    Randomly generate a string which contains 5-10 characters.
    :return: random string name
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.mark.order(before="settings_arg_setter_test.py::test_set_settings_arg")
def test_get_settings_arg(tmp_path: Path) -> None:
    """
    Test function "get_settings_arg".
    Create a temporary json file,
    write a dict into the file,
    use the function to test whether key and value exist.
    """
    dict_key: str = random_str()
    dict_value: str = random_str()
    tmp_dict: dict = {
        dict_key: dict_value,
    }

    tmp_file: Path = tmp_path / f"{random_str()}.json"
    tmp_file.write_text(json.dumps(tmp_dict))
    # assert
    res, value = get_settings_arg(dict_key, str(tmp_file.resolve()))
    assert res is True
    assert value == dict_value
    res, value = get_settings_arg("123", str(tmp_file.resolve()))
    assert res is False
    assert value == ""
    # clean
    tmp_file.unlink()
