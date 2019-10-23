from rdkit import Chem
import numpy as np


def postfilter_mols(molecule_query, mol_most_similars, atoms_to_grow, atoms_to_avoid, avoid_repetition):

    try:
        mols_after_filter = list(mol_most_similars); m_ref= [ m for m in molecule_query][0]
    except TypeError:
        mols_after_filter = list(mol_most_similars); m_ref= molecule_query

    if avoid_repetition:
        #Broken
        mol_most_similars = remove_duplicates(mol_most_similars)
    if any(atoms_to_grow):
        coords_grow, neighbors_grow, indexes_grow = retrieve_atom_info(m_ref, atoms_to_grow)
    if any(atoms_to_avoid):
        coords_avoid, neighbors_avoid, indexes_avoid = retrieve_atom_info(m_ref, atoms_to_avoid)
    for m in reversed(mols_after_filter):
        if any(atoms_to_grow):
            if not is_bonded(m_ref, m.molecule, atoms_to_grow, coords_grow, neighbors_grow, indexes_grow):
                mols_after_filter.remove(m)
                continue
        if any(atoms_to_avoid):
            if not is_not_bonded(m_ref, m.molecule, atoms_to_avoid, coords_avoid, neighbors_avoid, indexes_avoid):
                mols_after_filter.remove(m)
                continue
    return mols_after_filter

def remove_duplicates(molecules_duplicated):
    names = []
    mols_no_duplicates = []
    for mol in molecules_duplicated:
        name = mol.molecule.GetProp("_Name")
        if name in names:
            pass
        else:
            names.append(name)
            mols_no_duplicates.append(mol)
    return mols_no_duplicates

def retrieve_atom_info(m_ref, atoms):
    coords=[]; neighbors=[]; indexes=[]
    for atom in  m_ref.GetAtoms():
        if atom.GetIdx()+1 in atoms:
            indexes.append(atom.GetIdx())
            neighbors.append(len(atom.GetNeighbors()))
            coords.append(m_ref.GetConformer(0).GetPositions()[atom.GetIdx()])
    return coords, neighbors, indexes


def is_bonded(m_ref, mol, atoms, coords, neighbors, indexes):
    valid = False
    try:
        rmsd = Chem.rdMolAlign.AlignMol(mol, m_ref)
    except RuntimeError:
        try:
            rmsd = Chem.rdMolAlign.AlignMol(m_ref, mol)
        except RuntimeError:
            print("Skipped")
            return False
    for coord_ref, neighbour_ref, index_ref in zip(coords, neighbors, indexes):
        coords = mol.GetConformer(0).GetPositions()
        distances_to_atoms_from_ref = [np.linalg.norm(coord_ref - coord) for coord in coords]
        idx = np.argmin(distances_to_atoms_from_ref)
        min_distance_to_atomref = distances_to_atoms_from_ref[idx]
        if distances_to_atoms_from_ref[idx] > 0.4:
            return False
        atom = [ atom for i, atom in enumerate(mol.GetAtoms()) if i == idx][0]
        if len(atom.GetNeighbors()) > neighbour_ref:
            return True
    return False


def is_not_bonded(m_ref, mol, atoms, coords, neighbors, indexes):
    valid = False
    rmsd = Chem.rdMolAlign.AlignMol(m_ref, mol)
    for coord_ref, neighbour_ref, index_ref in zip(coords, neighbors, indexes):
        coords = mol.GetConformer(0).GetPositions()
        distances_to_atoms_from_ref = [np.linalg.norm(coord_ref - coord) for coord in coords]
        idx = np.argmin(distances_to_atoms_from_ref)
        min_distance_to_atomref = distances_to_atoms_from_ref[idx]
        print(min_distance_to_atomref)
        if distances_to_atoms_from_ref[idx] > 0.4:
            return False
        atom = [ atom for i, atom in enumerate(mol.GetAtoms()) if i == idx][0]
        if len(atom.GetNeighbors()) > neighbour_ref:
            return False
    return True







