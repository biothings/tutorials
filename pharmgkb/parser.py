import os, pandas, csv, re
import numpy as np
from biothings.utils.dataload import dict_convert, dict_sweep

from biothings import config
logging = config.logger


# we'll remove space in keys to make queries easier. Also, lowercase is preferred
# for a BioThings API. We'll an helper function from BioThings SDK
process_key = lambda k: k.replace(" ","_").lower()


def load_annotations(data_folder):
    infile = os.path.join(data_folder,"var_drug_ann.tsv")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict(orient='records')
    results = {}
    for rec in dat:
        if not rec["Gene"] or pandas.isna(rec["Gene"]):
            logging.warning("No gene information for annotation ID '%s'", rec["Annotation ID"])
            continue
        _id = re.match(".* \((.*?)\)",rec["Gene"]).groups()[0]
        rec = dict_convert(rec,keyfn=process_key)
        # remove NaN values, not indexable
        rec = dict_sweep(rec,vals=[np.nan])
        results.setdefault(_id,[]).append(rec)
    for _id,docs in results.items():
        doc = {"_id": _id, "annotations" : docs}
        yield doc


def load_druglabels(data_folder):
    infile = os.path.join(data_folder,"drugLabels.byGene.tsv")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict(orient='records') 
    for rec in dat:
        label_ids = rec.pop("Label IDs").split(";")
        label_names = rec.pop("Label Names").split(";")
        assert len(label_ids) == len(label_names)
        labels = []
        for i,_ in enumerate(label_ids):
            labels.append({"id" : label_ids[i],
                           "name" : label_names[i]})
        _id = rec["Gene ID"]
        rec = dict_convert(rec,keyfn=process_key)
        doc = {"_id" : _id, "drug_labels" : labels}
        yield doc


def load_occurrences(data_folder):
    infile = os.path.join(data_folder,"occurrences.tsv")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict(orient='records')
    results = {}
    for rec in dat:
        if rec["Object Type"] != "Gene":
            continue
        _id = rec["Object ID"]
        rec = dict_convert(rec,keyfn=process_key)
        results.setdefault(_id,[]).append(rec)
    for _id,docs in results.items():
        doc = {"_id": _id, "occurrences" : docs}
        yield doc

