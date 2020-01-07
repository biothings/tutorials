import os, pandas, csv, re
import math

from biothings import config
from biothings.utils.dataload import dict_convert
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
        # we'll remove space in keys to make queries easier. Also, lowercase is preferred
        # for a BioThings API. We'll an helper function from BioThings SDK
        process_key = lambda k: k.replace(" ","_").lower()
        rec = dict_convert(rec,keyfn=process_key)
        results.setdefault(_id,[]).append(rec)
        
    for _id,docs in results.items():
        doc = {"_id": _id, "annotations" : docs}
        yield doc
