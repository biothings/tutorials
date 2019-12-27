import os, pandas, csv, re
import numpy as np
from biothings.utils.dataload import dict_sweep

from biothings import config
logging = config.logger

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
        doc = {"_id" : rec["Gene ID"], "drug_labels" : labels}
        yield doc
