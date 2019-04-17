import os
import argparse
from analogs_finder.helpers import formats as ft
from analogs_finder.constants import constants as cs



class PhaseScreen():

    def __init__(self, query_mol, database):
        self.query_mol = query_mol
        self.database = database

    
    def create_pharmacophore_hypotesis(self, schr=cs.SCHR, output="query_molec.phypo"):
        hypotesis_bin =  os.path.join(schr, "utilities/create_hypoFiles")
        project_name = output.split(".")[:-1]
        command = "{} {} {} > /dev/null".format(hypotesis_bin, self.query_mol, project_name[0])
        print(command)
        os.system(command)
        self.hypotesis = output
        return self.hypotesis 
   
    def run(self, schr=cs.SCHR, output_project="query_molec_phase"):
        assert hasattr(self, "hypotesis"), "create_pharmacophore_hypotesis must be run before phase screening"
        phase_bin = os.path.join(schr, "phase_screen")
        command = "{} {} {} {}".format(phase_bin, self.database, self.hypotesis, output_project)
        print(command)
        os.system(command)
            

def run_phase_screen(query_mol, database):
    print("\n")
    print("Pharmacophore Screening")
    print("------------------------\n")
    print("Input query file: {}".format(query_mol))
    print("Database to screen: {}".format(database))
    print("\n")
    query_mol_mae = ft.sdf_to_mae(query_mol)
    phase = PhaseScreen(query_mol_mae, database)
    phase.create_pharmacophore_hypotesis()
    phase.run()
    

def parse_args(parser):
    parser.add_argument('--query_molec', type=str,
                        help='Reference molecule to create pharmacophores from')
    parser.add_argument('--database', type=str,
                        help='Database for pharmacophore screening')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pharmacophore Screening')
    parse_args(parser)
    args = parser.parse_args()
    run_phase_screen(args.query_molec, args.database)
    
