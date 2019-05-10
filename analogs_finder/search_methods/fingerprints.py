from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.Chem import MACCSkeys
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem import AllChem
from rdkit.Chem.Pharm2D import Gobbi_Pharm2D,Generate


def fingerprint(mol, fp_type="DL"):
    if fp_type == "DL":
        return FingerprintMols.FingerprintMol(mol)
    elif fp_type == "circular":
        return AllChem.GetMorganFingerprintAsBitVect(mol, 3, nBits=1024)
    elif fp_type == "MACCS":
        return MACCSkeys.GenMACCSKeys(mol)
    elif fp_type == "torsions":
        return Pairs.GetAtomPairFingerprintAsBitVect(mol)
    elif fp_type == "pharm":
        return Generate.Gen2DFingerprint(mol,Gobbi_Pharm2D.factory) 

