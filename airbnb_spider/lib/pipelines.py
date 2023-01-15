# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import rootpath
from scrapy.exporters import BaseItemExporter

ROOT_PATH = Path(rootpath.detect(__file__))


class PandasItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.file = file
        dt_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.interval = 30
        self._reset()

    def finish_exporting(self):
        self._save()
        self.df = pd.DataFrame()

    def export_item(self, item):
        self.df = pd.concat([self.df, pd.DataFrame([item])], axis=0)
        if time.time() - self._start_time > self.interval:
            self._save()
            self._reset()
        return item

    def _reset(self):
        self._start_time = time.time()
        self.df = pd.DataFrame()

    def _save(self):
        dt_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{dt_str}.pkl.zip"
        self.df.to_pickle(self.file)


class ResultsDirPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        params = crawler.settings["PARAMS"]
        dt_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = ROOT_PATH / f"results/{dt_str}_{params.name}_{params.start_date}_{params.end_date}"
        return cls(path=path)

    def __init__(self, path):
        self.path = path
        self.interval = 30
        self._reset()

    def _reset(self):
        self._start_time = time.time()
        self.df = pd.DataFrame()

    def process_item(self, item, spider):
        self.df = pd.concat([self.df, pd.DataFrame([item])], axis=0)
        if time.time() - self._start_time > self.interval:
            self._save()
            self._reset()
        return item

    def close_spider(self, spider):
        self._save()
        self.df = pd.DataFrame()

    def _save(self):
        dt_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{dt_str}.pkl.zip"
        self.path.mkdir(parents=True, exist_ok=True)
        self.df.to_pickle(self.path / file_name)
