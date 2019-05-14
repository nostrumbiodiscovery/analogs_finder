from tqdm import tqdm
import numpy as np
from rdkit import Chem
from rdkit import DataStructs
from analogs_finder.search_methods import fingerprints as fps
from analogs_finder.search_methods import molecule as ml


def compute_similarity(mref, molecules, fp_type="DL"):
    fp_ref = fps.fingerprint(mref, fp_type)
    for i, m in enumerate(molecules):
        if m:
            yield ml.molec_properties(m, fp_ref=fp_ref, fp_type=fp_type)
        else:
            print("Molecule {}".format(i))

def compute_similarity_severl_fp(mref, molecules, fp_types=["DL", "circular", "torsions", "MACCS"], tresholds=[0.7, 0.4, 0.7, 0.4]):
    for i, m in tqdm(enumerate(molecules)):
        chosen = False
        for j, fp_type in enumerate(fp_types):
            fp_ref = fps.fingerprint(mref, fp_type=fp_type)
            if not chosen:
                if m:
                    molec = ml.molec_properties(m, fp_ref=fp_ref, fp_type=fp_type)
                    if molec.similarity > float(tresholds[j]):
                        chosen = True
                        yield molec
                else:
                    print("Molecule {}".format(i))
            else:
                break

def compute_similarity_several_mols(mrefs, molecules, fp_type="DL"):
    fp_refs = [ fps.fingerprint(mref, fp_type=fp_type) for mref in mrefs if mref ]
    for m in molecules:
        if m:
            molec = ml.molec_properties(m, fp_type=fp_type)
            molec.similarities = [DataStructs.FingerprintSimilarity(fp_ref, molec.fp) for fp_ref in fp_refs ]
            yield molec
        else:
            pass
