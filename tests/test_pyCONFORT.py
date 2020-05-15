#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
import pandas as pd
import subprocess
import DBGEN

# saves the working directory
path = os.getcwd()

def read_energies(file): # parses the energies from sdf files - then used to filter conformers
	energies = []
	f = open(file,"r")
	readlines = f.readlines()
	for i in range(len(readlines)):
		if readlines[i].find('>  <Energy>') > -1:
			energies.append(float(readlines[i+1].split()[0]))
	f.close()
	return energies

# tests for the DBGEN module with organic molecules
@pytest.mark.parametrize("smiles, params_file, n_confs, prefilter_confs_rdkit, filter_confs_rdkit, E_confs, charge",
[
    ('pentane.smi', 'params_test1.yaml', 240, 236, 0, [-5.27175,-4.44183,-3.84858,-1.57172],0), # test sample = 'auto', auto_sample = 20
    ('pentane.smi', 'params_test2.yaml', 20, 16, 0, [-5.27175,-4.44183,-3.84858],0), # test sample = 20
    ('pentane.smi', 'params_test3.yaml', 20, 2, 13, [-5.27175,-4.44183,-3.84858,-1.57172],0), # test initial_energy_threshold = 1E-10
    ('pentane.smi', 'params_test4.yaml', 20, 10, 0, [-5.27175,-5.27175,-5.27175,-4.44183,-4.44183,-4.44183,-3.84858],0), # test energy_threshold = 1E-15
    ('pentane.smi', 'params_test5.yaml', 20, 10, 0, [-5.27175,-5.27175,-5.27175,-4.44183,-4.44183,-4.44183,-3.84858],0), # test rms_threshold = 1E-15
    ('pentane.smi', 'params_test6.yaml', 20, 2, 11, [-5.27175,-4.44183,-4.44183,-4.44183,-4.44183,-3.84858],0),
    ('pentane.smi', 'params_test7.yaml', 60, 56, 0, [-5.27175,-4.44183,-3.84858,-1.57172],0), # test sample = 'auto', auto_sample = 5
    ('pentane.smi', 'params_test8.yaml', 'nan', 'nan', 'nan', 'nan', 'nan'), # test num_rot_bonds = 1
    ('pentane.smi', 'params_test9.yaml', 'nan', 'nan', 'nan', 'nan', 'nan'), # test max_MolWt = 1
    ('pentane.smi', 'params_test10.yaml', 20, 16, 0, [2.52059,3.68961,4.94318],0), # test ff = 'UFF'
    ('pentane.smi', 'params_test11.yaml', 20, 0, 8, [-5.27037,-4.82921,-4.43450,-4.42888,-3.78645,-3.48832],0), # test opt_steps_RDKit = 40
    ('pentane.smi', 'params_test12.yaml', 20, 16, 0, [-5.27175,-4.44183,-3.84858,-1.57172],0), # test seed = 10
])

def test_confgen(smiles, params_file, n_confs, prefilter_confs_rdkit, filter_confs_rdkit, E_confs, charge):
	# gets into the directory for testing SMILES
	os.chdir(path+'/'+smiles.split('.')[0])

	# Conformer generation using different parameters. It creates a CSV file
	subprocess.run(['python', '-m', 'DBGEN', '--varfile', params_file])

	# Retrieving the generated CSV file
	df_output = pd.read_csv(smiles.split('.')[0]+'-Duplicates Data.csv')

	file = params_file.split('.')[0]

	# tests for RDKit
	test_init_rdkit_confs = df_output['RDKIT-Initial-samples']
	test_prefilter_rdkit_confs = df_output['RDKit-energy-duplicates']
	test_filter_rdkit_confs = df_output['RDKit-RMSD-and-energy-duplicates']

	assert str(n_confs) == str(test_init_rdkit_confs[0])
	assert str(prefilter_confs_rdkit) == str(test_prefilter_rdkit_confs[0])
	assert str(filter_confs_rdkit) == str(test_filter_rdkit_confs[0])

	# read the energies of the conformers
	os.chdir(path+'/'+smiles.split('.')[0]+'/RDKit_generated_SDF_files')
	test_rdkit_E_confs = read_energies(smiles.split('.')[0]+'_rdkit.sdf')

	# test for energies
	round_confs = [round(num, 3) for num in E_confs]
	if len(test_rdkit_E_confs) > 1:
		test_round_confs = [round(num, 3) for num in test_rdkit_E_confs]

	assert str(round_confs) == str(test_round_confs)

	# tests charge
	test_charge = df_output['Overall charge']

	assert str(charge) == str(test_charge[0])

# MISSING CHECKS:
# CHECK COM FILES generation
# CHECK THAT THE METAL PART IS WORKING
# CHECK THAT MULTIPLE METALS ARE COMPATIBLE
# CHECK THAT THE TEMPLATE PART IS WORKING
# CHECK THAT THE EXPEIRMENTAL RULES IS WORKING
# CHECK THAT ANALYSIS IS WORKING FROM ALL THE DIFFERENT FOLDERS (USE SMALL TEST LOG FILES WITH ALL THE TYPE OF ERRORS)
# CHECK THAT AUTOPREP IS WORKING
# CHECK THAT GENECP AND GEN IS WORKING