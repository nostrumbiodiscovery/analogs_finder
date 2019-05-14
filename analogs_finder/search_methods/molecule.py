from analogs_finder.search_methods import fingerprints as fps
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import AllChem


class Molecule(object):

    def __init__(self, molecule):
        self.molecule = molecule
        self.fp = None
        self.similarity = None


    def compute_similarity(self, fp_ref):
        self.fp_ref = fp_ref
        self.similarity = DataStructs.FingerprintSimilarity(self.fp_ref, self.fp)
        return self.similarity


    def compute_fp(self, fp_type):
        self.fp_type = fp_type
        self.fp = fps.fingerprint(self.molecule, fp_type=self.fp_type)
        return self.fp

    def to_svg(self, molSize=(300,300), kekulize=True):
        mc = Chem.Mol(self.molecule.ToBinary())
        if kekulize:
            try:
                Chem.Kekulize(mc)
            except:
                mc = Chem.Mol(self.molecule.ToBinary())
        if not mc.GetNumConformers():
            mc = AllChem.Compute2DCoords(mc)
        AllChem.Compute2DCoords(mc)
        drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])
        drawer.DrawMolecule(mc)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        return svg.replace('svg:','')
        

def molec_properties(m, fp_ref=None, fp_type=None):
    molec = Molecule(m)
    if fp_type:
        molec.compute_fp(fp_type)
    if fp_ref:
        molec.compute_similarity(fp_ref)
    return molec
