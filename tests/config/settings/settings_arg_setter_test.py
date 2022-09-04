import json
import random
import string
from pathlib import Path

from splasher.config.settings import get_settings_arg, set_settings_arg


def random_str(length: int = random.randint(5, 10)) -> str:
    """
    Randomly generate a string which contains 5-10 characters.
    :return: random string name
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def test_set_settings_arg(tmp_path: Path) -> None:
    """
    Test function "set_settings_arg".
    Create a temporary json file,
    write a dict into the file and modify the value,
    use the function to test whether key and value exist.
    """
    dict_key: str = random_str()
    dict_value: str = random_str()
    tmp_dict: dict = {
        dict_key: "",
    }

    tmp_file: Path = tmp_path / f"{random_str()}.json"
    tmp_file.write_text(json.dumps(tmp_dict))
    # assert
    res: bool = set_settings_arg("123", dict_value, str(tmp_file.resolve()))
    assert res is False
    res: bool = set_settings_arg(dict_key, dict_value, str(tmp_file.resolve()))
    assert res is True
    res, value = get_settings_arg(dict_key, str(tmp_file.resolve()))
    assert res is True
    assert value == dict_value
    # clean
    tmp_file.unlink()
