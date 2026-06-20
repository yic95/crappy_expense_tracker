import pathlib
import csv
import datetime as dt
import time

class TagsService:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)
        self.tags = []
        self.tags = self.read()
        if not self.data_dir.is_dir():
            raise ValueError(f'{data_dir} is not a directory')

    def read(self):
        tags_path = self.data_dir / 'tags.txt'
        if not tags_path.exists():
            self.tags = []
        elif not self.tags or tags_path.stat().st_mtime > time.time():
            with tags_path.open('r', encoding='utf-8', newline='') as f:
                self.tags = f.read().split()
        return self.tags

    def delete(self, name: str):
        tags = self.read()
        tags = [s for s in tags if s != name]
        tags_path = self.data_dir / 'tags.txt'
        if not tags_path.exists():
            return
        with tags_path.open('w', encoding='utf-8', newline='') as f:
            for t in tags:
                f.write(f"{t}\n")
        self.tags = tags

    def write(self, name: str):
        tags_path = self.data_dir / 'tags.txt'
        tags = self.read()
        with tags_path.open('w', encoding='utf-8', newline='') as f:
            for t in tags:
                f.write(f"{t}\n")
            f.write(f"{name}\n")
        tags.append(name)
        self.tags = tags
