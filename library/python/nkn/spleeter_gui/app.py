import dataclasses
import subprocess
from pathlib import Path

from nkn.core import config
from nkn.core.env import Env, EnvKey


@dataclasses.dataclass
class App(config.DataInterface):
    def get_path(self) -> Path:
        return config.PYTHON_SCRIPTS_PATH.joinpath('spleeter.exe')

    def get_env(self) -> Env:
        env = Env()
        return env

    def execute(self, args) -> None:
        path = self.get_path()
        cmd = [
                  str(path),
              ] + args
        env = self.get_env().to_dict()
        subprocess.Popen(
            cmd,
            env=env,
            shell=True,
        )
