#!/usr/bin/env python

######################################################.
# 	        Testing QCORR with pytest                #
#           using the exp_rules filter	             #
######################################################.

import os
import glob
import pytest
from definitions_testing import analysis,single_point

# saves the working directory
path_analysis_qcorr = os.getcwd()

# tests for individual organic molecules and metal complexes
@pytest.mark.parametrize("folder, params_file",
[
    # tests of the QCORR part
    ('QCORR_Geom_check_exp_rules', 'params_QCORR_test.yaml') # test exp_rules and check_geom options
])

def test_analysis_qcorr_exp_rules(folder, params_file):
    # runs the program with the different tests
    cmd_aqme = ['python', '-m', 'aqme', '--varfile', params_file]

    df_QCORR, _ = analysis(path_analysis_qcorr, cmd_aqme, folder, 'csv')

    # ensure that the CSV includes all the results
    assert df_QCORR['Total files'][0] == 4
    assert df_QCORR['Normal termination'][0] == 1
    assert df_QCORR['Imaginary frequencies'][0] == 0
    assert df_QCORR['SCF error'][0] == 0
    assert df_QCORR['Basis set error'][0] == 0
    assert df_QCORR['Other errors'][0] == 0
    assert df_QCORR['Unfinished'][0] == 0
    assert df_QCORR['Exp_rules filter'][0] == 1
    assert df_QCORR['Geometry changed'][0] == 2

    # all the files are moved from the original directory
    os.chdir(path_analysis_qcorr+'/'+folder)
    assert len(glob.glob('*.LOG')) == 0
    assert len(glob.glob('*.log')) == 0
    assert len(glob.glob('*.out')) == 0
    assert len(glob.glob('*.OUT')) == 0

    # look for the LOG files
    os.chdir(path_analysis_qcorr+'/'+folder+'/success/output_files')
    assert len(glob.glob('*.log')) == 1
    os.chdir(path_analysis_qcorr+'/'+folder+'/failed/run_1/exp_rules_filter')
    assert len(glob.glob('*.log')) == 1
    os.chdir(path_analysis_qcorr+'/'+folder+'/failed/run_1/geometry_changed')
    assert len(glob.glob('*.log')) == 2

    # look for the COM files
    os.chdir(path_analysis_qcorr+'/'+folder+'/success/G16-SP_input_files')
    assert len(glob.glob('*.com')) == 1

    # this tests that when the last line option for SP is deactivated, the program does not print None in the com file
    com_file = glob.glob('*.com')[0]

    outfile = open(com_file,"r")
    outlines = outfile.readlines()

    last_line_found = False
    for line in outlines:
        if line.find('None') > -1:
            last_line_found = True

    assert last_line_found == False

    outfile.close()
