import os

import biothings, config
biothings.config_for_app(config)

import biothings.hub.dataload.uploader

# when code is exported, import becomes relative
try:
    from pharmgkb.parser import load_annotations as parser_func
except ImportError:
    from .parser import load_annotations as parser_func


class PharmgkbUploader(biothings.hub.dataload.uploader.BaseSourceUploader):

    name = "pharmgkb"
    __metadata__ = {"src_meta": {}}
    idconverter = None
    storage_class = biothings.hub.dataload.storage.BasicStorage

    def load_data(self, data_folder):
        self.logger.info("Load data from directory: '%s'" % data_folder)
        return parser_func(data_folder)

    @classmethod
    def get_mapping(klass):
        return         {
            'annotations': {
                'properties': {
                    'Alleles': {
                        'type': 'text'
                    },
                    'Annotation ID': {
                        'type': 'integer'
                    },
                    'Chemical': {
                        'type': 'text'
                    },
                    'Chromosome': {
                        'normalizer': 'keyword_lowercase_normalizer',
                        'type': 'keyword'
                    },
                    'Gene': {
                        'type': 'text'
                    },
                    'Notes': {
                        'type': 'text'
                    },
                    'PMID': {
                        'type': 'integer'
                    },
                    'Phenotype Category': {
                        'normalizer': 'keyword_lowercase_normalizer',
                        'type': 'keyword'
                    },
                    'Sentence': {
                        'type': 'text'
                    },
                    'Significance': {
                        'type': 'text'
                    },
                    'StudyParameters': {
                        'normalizer': 'keyword_lowercase_normalizer',
                        'type': 'keyword'
                    },
                    'Variant': {
                        'type': 'text'
                    }
                }
            }
        }

