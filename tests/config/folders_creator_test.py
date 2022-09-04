import os
import random
import shutil
import string

import pytest

from splasher.config import PATH
from splasher.config.folders_creator import create_folder, create_folders


@pytest.mark.order(before="settings/settings_creator_test.py::test_create_settings")
class TestFolderCreator:
    """
    A class to test functions in "splasher/config/folders_creator.py"
    """

    def random_str(self, length: int = random.randint(5, 10)) -> str:
        """
        Randomly generate a string which contains 5-10 characters.
        :return: random string name
        """
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    def test_create_folder(self) -> None:
        """
        Test function "create_folder".
        Execute "create_folder" to create a random directory in "/tmp", and create a subfolder in it.
        Test whether these two folders exist or not.
        """
        dir_path: str = f"/tmp/{self.random_str()}/"
        subfolder_name: str = f"{self.random_str()}/"
        # assert
        create_folder(dir_path, subfolder_name)
        assert os.path.isdir(dir_path) is True
        assert os.path.isdir(f"{dir_path}{subfolder_name}") is True
        # clean
        shutil.rmtree(dir_path)

    def test_create_folders(self) -> None:
        """
        Test function "create_folders".
        If folders required by the app are already exist, move them to "/tmp".
        Execute "create_folders" to create corresponding directories.
        Delete newly created directories, and move folders in "/tmp" back to original paths.
        """
        # move current dirs to "/tmp"
        tmp_cache: str = f"/tmp/{self.random_str()}"
        if os.path.isdir(PATH["CACHE"]):
            shutil.move(PATH["CACHE"], tmp_cache)
        tmp_config: str = f"/tmp/{self.random_str()}"
        if os.path.isdir(PATH["CONFIG"]):
            shutil.move(PATH["CONFIG"], tmp_config)
        tmp_log: str = f"/tmp/{self.random_str()}"
        cur_log: str = f"{os.getcwd()}/logs/"
        if os.path.isdir(cur_log):
            shutil.move(cur_log, tmp_log)
        tmp_background: str = f"/tmp/{self.random_str()}"
        if os.path.isdir(PATH["BACKGROUND"]):
            shutil.move(PATH["BACKGROUND"], tmp_background)
        # assert
        create_folders()
        assert os.path.isdir(PATH["CACHE"]) is True
        assert os.path.isdir(f"{PATH['CACHE']}{PATH['SUBFOLDER']}") is True
        assert os.path.isdir(PATH["CONFIG"]) is True
        assert os.path.isdir(cur_log) is True
        assert os.path.isdir(PATH["BACKGROUND"]) is True
        # move back
        if os.path.isdir(tmp_cache):
            shutil.rmtree(PATH["CACHE"])
            shutil.move(tmp_cache, PATH["CACHE"])
        if os.path.isdir(tmp_config):
            shutil.rmtree(PATH["CONFIG"])
            shutil.move(tmp_config, PATH["CONFIG"])
        if os.path.isdir(tmp_log):
            shutil.rmtree(cur_log)
            shutil.move(tmp_log, cur_log)
        if os.path.isdir(tmp_background):
            shutil.rmtree(PATH["BACKGROUND"])
            shutil.move(tmp_background, PATH["BACKGROUND"])
