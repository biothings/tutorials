import os

import biothings, config
biothings.config_for_app(config)
from config import DATA_ARCHIVE_ROOT

from biothings.utils.common import uncompressall

import biothings.hub.dataload.dumper


class PharmgkbDumper(biothings.hub.dataload.dumper.LastModifiedHTTPDumper):

    SRC_NAME = "pharmgkb"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)
    SCHEDULE = None
    UNCOMPRESS = True
    SRC_URLS = [
        'https://s3.pgkb.org/data/annotations.zip',
        'https://s3.pgkb.org/data/drugLabels.zip',
        'https://s3.pgkb.org/data/occurrences.zip'
    ]
    __metadata__ = {"src_meta": {}}

    def post_dump(self, *args, **kwargs):
        if self.__class__.UNCOMPRESS:
            self.logger.info("Uncompress all archive files in '%s'" %
                             self.new_data_folder)
            uncompressall(self.new_data_folder)
