from rdkit import Chem



def molecules_to_sdf(molecules, output):
    w = Chem.SDWriter(output)
    n_mol_found = 0
    for molecule in molecules: 
        w.write(molecule.molecule)
        n_mol_found += 1
    return n_mol_found
