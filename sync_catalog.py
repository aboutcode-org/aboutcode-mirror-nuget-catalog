#
# Copyright (c) nexB Inc. and others. All rights reserved.
# VulnerableCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
from datetime import datetime
from datetime import timezone
from pathlib import Path

import requests

from aboutcode.pipeline import BasePipeline
from aboutcode.pipeline import LoopProgress

ROOT_PATH = Path(__file__).parent
CATALOG_PATH = ROOT_PATH / "catalog"
CATALOG_INDEX = CATALOG_PATH / "index.json"
PAGE_DIRECTORY = CATALOG_PATH / "pages"


class NuGetCatalogMirror(BasePipeline):
    url = "https://api.nuget.org/v3/catalog0/"

    @classmethod
    def steps(cls):
        return (
            cls.check_new_catalog,
            cls.collect_new_catalog,
        )

    def check_new_catalog(self):
        start_page = self.get_catalog_page_count()
        self.fetch_and_write(f"{self.url}/index.json", CATALOG_INDEX)
        end_page = self.get_catalog_page_count()
        self.pages_to_collect = range(start_page, end_page)

    def collect_new_catalog(self):
        latest_pages = list(self.pages_to_collect)
        page_count = len(latest_pages)
        self.log(f"Collecting {page_count:,d} latest catalog pages.")
        progress = LoopProgress(
            total_iterations=page_count,
            logger=self.log,
        )
        for page in progress.iter(latest_pages):
            page_id = f"page{page}"
            self.fetch_and_write(
                url=f"{self.url}{page_id}.json",
                path=PAGE_DIRECTORY / f"{page_id}.json",
            )

    def log(self, message):
        now_local = datetime.now(timezone.utc).astimezone()
        timestamp = now_local.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        message = f"{timestamp} {message}"
        print(message)

    def fetch(self, url):
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json() or {}

    def get_catalog_page_count(self):
        if CATALOG_INDEX.exists():
            with CATALOG_INDEX.open("r", encoding="utf-8") as f:
                index = json.load(f)
                return index.get("count", 0)
        return 0

    def fetch_and_write(self, url, path):
        response = self.fetch(url)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=2)


if __name__ == "__main__":
    error, error_msg = NuGetCatalogMirror().execute()
    if error:
        print(error_msg)
