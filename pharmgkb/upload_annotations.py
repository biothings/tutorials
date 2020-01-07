import os

import biothings, config
biothings.config_for_app(config)

import biothings.hub.dataload.uploader

from .parser import load_annotations


class AnnotationsUploader(biothings.hub.dataload.uploader.BaseSourceUploader):

    main_source = "pharmgkb"
    name = "annotations"
    __metadata__ = {"src_meta": {}}
    idconverter = None
    storage_class = biothings.hub.dataload.storage.BasicStorage

    def load_data(self, data_folder):
        self.logger.info("Load data from directory: '%s'" % data_folder)
        return load_annotations(data_folder)

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

