import json

import dataclasses
from pathlib import Path

from nkn.core import util

ROOT_PATH: Path = Path(__file__).joinpath('..', '..', '..', '..', '..').resolve()
CONFIG_FILE: Path = ROOT_PATH.joinpath('data', 'app', 'SpleeterGUI.json')
PYTHONW_EXE_PATH: Path = ROOT_PATH.joinpath(
    json.loads(CONFIG_FILE.read_text(encoding='utf-8'))['program']
)
CONFIG_DIR: Path = ROOT_PATH.joinpath('config')
DATA_PATH = ROOT_PATH.joinpath('data')
BIN_PATH = ROOT_PATH.joinpath('bin')

PYTHON_INSTALL_PATH: Path = PYTHONW_EXE_PATH.parent
PYTHON_EXE_PATH = PYTHON_INSTALL_PATH.joinpath('python.exe')
PYTHON_SCRIPTS_PATH = PYTHON_INSTALL_PATH.joinpath('Scripts')


class DataList(list):
    def __init__(self, cls):
        super().__init__()
        self._data_cls = cls

    def new_data(self):
        return self._data_cls()

    def set(self, lst: list):
        self.clear()
        for i in lst:
            data = self._data_cls()
            data.set(i)
            self.append(data)

    def set_list(self, lst: list):
        self.clear()
        for i in lst:
            self.append(i)

    def to_list(self) -> list:
        lst = []
        for i in self:
            lst.append(i)
        return lst

    def to_list_of_dict(self) -> list:
        lst = []
        for i in self:
            lst.append(dataclasses.asdict(i))
        return lst


@dataclasses.dataclass
class DataInterface:
    def set(self, dct):
        base = dataclasses.asdict(self)
        for k in base.keys():
            if k in dct:
                if isinstance(getattr(self, k), DataInterface):
                    getattr(self, k).set(dct[k])
                elif isinstance(getattr(self, k), DataList):
                    getattr(self, k).set(dct[k])
                else:
                    setattr(self, k, dct[k])

    def as_dict(self) -> dict:
        dct = dataclasses.asdict(self)
        for k in dct.keys():
            if isinstance(getattr(self, k), DataList):
                dct[k] = getattr(self, k).to_list_of_dict()
        return dct


@dataclasses.dataclass
class Data(DataInterface):
    def load(self, path: Path) -> None:
        dct = json.loads(path.read_text(encoding='utf-8'))
        self.set(dct)

    def save(self, path: Path) -> None:
        util.write_text(
            path,
            json.dumps(self.as_dict(), indent=2, ensure_ascii=False),
        )


if __name__ == '__main__':
    @dataclasses.dataclass
    class D(DataInterface):
        a: int = 10


    dl = DataList(D)
    print(dl)
    dl.set(
        [
            {'a': 10},
            {'a': 20},
            {'a': 30},
        ]
    )
    print(dl)
