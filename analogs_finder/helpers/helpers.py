


def remove_duplicates(molecules_duplicated):
    names = []
    mols_no_duplicates = []
    for mol in molecules_duplicated:
        name = mol.GetProp("_Name")
        if name in names:
            pass
        else:
            names.append(name)
            mols_no_duplicates.append(mol)
    return mols_no_duplicates
           
