.. _defaults:

===============================
Default and Required Parameters
===============================

This documents details the default parameters used in the ``aqme`` program.

.. contents::

Required parameters
-------------------
.. code-block:: yaml

  # INPUT FILE
  input : 'file.smi' # input files
  path : '/path/to/gaussian/folder/' # path to guassian folder when we do analysis

Output Parameters
-----------------
.. code-block:: yaml

  # OUTPUT PARAMETERS
  verbose : True
  prefix : False # if prefix : True, set a generic name for the different molecules (i.e. comp_1, comp_2, etc)

  # OUTPUT FILE NAMES
  output_name : 'output' #Change output filename to aqme_\"output\".dat


Options
-------
.. code-block:: yaml

  # (1) CONFORMERS AND COM FILES GENERATION
  # 3 options:
  # Compute : True and write_gauss : True --> generates conformers in SDF files and writes COM files
  # Compute : True and write_gauss : False --> generates conformers in SDF files only
  # Compute : False and write_gauss : True --> reads SDF files from the main DBGEN folder (all SDF files)

  compute : True
  write_gauss : True # writting Gaussian COM files after, look options of write_gauss below

  # (2) ANALYSIS OF LOG FILES
  # if analysis is True, check all LOG files inside "generated_gaussian_files".
  # The folder might multiple subfolders with levels of theory (i.e. coming from the conformer generation).
  # This generates new COM files from LOG files with imaginary freqs or errors

  analysis : False
  sp : False # write COM files after analysis
  dup : False # if dup : True, analysis will also separate duplicate LOG files
  boltz : False # if boltz : True, analysis will calculate Bolztmann probabilities of each conformer
  combine : False # if boltz : True and combine : True, all the data from the CSV files created with boltz will be condensed in 3 CSV files


Common Parameters to Edit
-------------------------

.. code-block:: yaml

  # COMMON PARAMETERS TO EDIT

  # (1) CHARGE FOR XTB OPTIMIZATION AND COM FILES
  charge : [] # final charge of the molecule (used in xTB optimization automatically updated for each metal atom if not charge_default is written)
  # If metal_complex : True, the script will recalculate the charge
  charge_default : 0 #used to write the default if cannot be calculated for metal atom

  # (2) TYPE OF OPTIMIZATION
  # Options: xTB, ANI1ccx (if True is selected).  Default : RDKit optimizaiton
  ANI1ccx : False
  xtb : False

  # (3) DIHEDRAL PROTOCOL FOR RDKIT OPTIMIZATION (SLOW SINCE IT SCANS MANY DIHEDRALS)
  nodihedrals : True # turn to True if no dihedral scan is needed
  degree : 30 # amount, in degrees, to enumerate torsions if nodihedrals is False

  # (4) RDKit AND xTB PARAMETERS
  ewin_min : 40 #energy window in kcal/mol to use conformers for ANI1ccx and xTB (conformers with E higher than ewin will be discarded)
  ewin_rdkit : 40 #energy window to print conformers for RDKit (kcal/mol)(conformers with E higher than ewin will be discarded)
  sample : 20 # number of conformers to sample to get non-torsional differences (default 100)

  # (5) OPTIONS FOR COM FILE GENERATION (write_gauss : True)
  # By default, you include optimization in the COM files.
  # Optional:
  frequencies : True # include frequency calculation
  single_point : False # do not include optimization

  # (5.1) ONLY LOWEST ENERGY CONFORMERS REQUIRED"
  lowest_only : False
  lowest_n : False # for a given threshold of energy_threshold_for_gaussian
  energy_threshold_for_gaussian : 100  # in kcal/mol, from all the conformers generated after xTB optimization
  # lowest_n must be True to apply this energy threshold

  # (5.2) DEFINITION OF A SECOND CATEGORY OF ATOMS SEPARATED IN GENECP
  genecp_atoms : [] # list of atoms included in the gen_ecp part
  gen_atoms : [] # list of atoms inclueded in gen part

  # (5.3) DEFINTION OF BASIS SET AND LEVEL OF THEORY AND SOLVENT
  basis_set : ['def2svp'] # basis set
  basis_set_genecp_atoms : ['LANL2DZ'] # functional for the genecp part
  level_of_theory : ['wb97xd'] # functional

  # (5.4) DISPERSION CORRECTION FOR COM FILES
  dispersion_correction : False # include dispersion correction
  empirical_dispersion : 'GD3BJ' # type of dispersion correction

  # (5.5) SOLVATION MODEL
  solvent_model : 'gas_phase' # type of solvation model. Options: gas_phase or any solvation model (i.e. SMD, IEFPCM, CPCM)
  solvent_name : 'Chloroform' # solvent

  # (5.6) DEFINITION OF A SECOND CATEGORY OF ATOMS SEPARATED IN GENECP FOR SINGLE POINT
  genecp_atoms_sp : [] # list of atoms included in the gen_ecp part
  gen_atoms_sp : [] # list of atoms inclueded in gen part

  # (5.7) DEFINTION OF BASIS SET AND LEVEL OF THEORY AND SOLVENT FOR SINGLE POINT
  basis_set_sp : ['def2svp'] # basis set
  basis_set_genecp_atoms_sp : ['LANL2DZ'] # functional for the genecp part
  level_of_theory_sp : ['wb97xd'] # functional

  # (5.8) DISPERSION CORRECTION FOR COM FILES FOR SINGLE POINT
  dispersion_correction_sp : False # include dispersion correction
  empirical_dispersion_sp : 'GD3BJ' # type of dispersion correction

  # (5.9) SOLVATION MODEL FOR SINGLE POINT
  solvent_model_sp : 'gas_phase' # type of solvation model. Options: gas_phase or any solvation model (i.e. SMD, IEFPCM, CPCM)
  solvent_name_sp : 'Chloroform' # solvent

  # (5.10) INPUT LINE AND LAST LINE FOR SINGLE POINT
  input_for_sp : 'nmr=giao' #Input line for Single point after DFT optimization
  last_line_for_sp : '' #Last input line for Single point after DFT optimization


  # (5.10) DEFAULT PARAMETERS FOR GAUSSIAN OPTIMIZATION
  chk : False # include a %chk line at the beginning of the COM file
  nprocs : 36 # number of processors for the COM file in %nprocshared
  mem: '60GB' # amount of memory for the COM file in %mem
  max_cycle_opt : 100 #default is 300

  # (6) PERFORMANCE OF THE CODE
  time : True #request run time

  # (7) OPTIONS FOR METALS, ATOMS WITH UNCOMMON HYBRIDIZATIONS AND NCI COMPLEXES
  # IF A METAL OR AN ATOM WITH UNCOMMON HYBRIDIZATION (i.e. pentacoordinated phosphorus) IS USED
  metal_complex : False # specify True to activate this option
  metal : [] # specify the metal(s) or atom(s) with uncommon hybridization, in the format 'A','B','C'...
  m_oxi : [] # oxidation number of the atom (it is used to calculate the charge of the molecule)
  complex_spin : 1 # final spin of the molecule (the code does not calculate spin, it must be defined by the user)

  # (8) EXP RULES
  exp_rules : False # apply some experimental rules to discard some outputs
  angle_off : 30 # margin of error to determine angles (i.e. if angle_off is 30, and the angle is 180, angles from
  # 150 to 210 degrees will be discarded)

  # (9) OPTIONS FOR THE AUTOMATED WORKFLOW
  qsub : False # turn on automated submission and analysis of jobs
  submission_command : 'qsub_summit' # name of the file containing the submission script


Pre-Optimised Parameters
------------------------

.. code-block:: yaml

  # (1) FOR UNIQUE CONFORMER SELECTION FOR RDKIT, XTB AND ANI1
  rms_threshold : 0.25 #cutoff for considering sampled conformers the same (default 0.25) for RDKit and xTB duplicate filters
  energy_threshold : 0.25 # energy difference in kcal/mol between unique conformers for RDKit and xTB duplicate filters
  initial_energy_threshold : 0.0001 # energy difference for the first RDKit filter based on E only
  max_matches_RMSD : 1000 # max iterations to find optimal RMSD in RDKit duplicate filter
                              # The higher the number the longer the duplicate filter takes but
                              # the more duplicates are filtered off
  heavyonly : True # If True, H from OH, NH, etc. will not be used to generate conformers (recommended: False with molecules that contain OH groups)
  auto_sample : 20 # final factor to multiply in the auto mode for the sample option (default 20)

  # (2) FILTERS FOR RDKIT OPTIMIZATION
  max_torsions : 20 # Skip any molecules with more than this many torsions (default 5)
  num_rot_bonds : 20 # Skip any molecules with more than this many rotatable bonds (default 5)
  max_MolWt : 10000 # Skip any molecules with molecular weights higher than this number

  # (3) PARAMETERS FOR RDKIT OPTIMIZATION
  ff : "MMFF" # force field used in the RDKit optimization. Options: MMFF or UFF
  etkdg : False # use new ETKDG knowledge-based method instead of distance geometry also needs to be present in RDKIT ENV
  seed : 62609 # random seed (default 62609) for ETKDG
  opt_steps_RDKit : 1000

  # (4) DEFAULT PARAMETERS FOR ANI1 and xTB OPTIMIZATION
  opt_steps : 1000 # max number of cycles during optimization
  opt_fmax : 0.05 # fmax value to achieve optimization

  # (5) DEFAULT PARAMETERS ONLY FOR ANI1 OPTIMIZATION
  constraints : None

  # (6) DEFAULT PARAMETERS ONLY FOR xTB OPTIMIZATION
  large_sys : True
  STACKSIZE : '1G' # set for large system


  # (7) METAL VARIABLES CALCULATED IN THE PROGRAM
  complex_coord : [] # specify the coordination number of the metal atom
  metal_idx : []
  metal_sym : []

  # (8) FIXED OUTPUT PARAMETERS
  output : '.sdf' # Required to be sdf files

  # (9) FIXED PARAMETER FOR IMAGINARY FREQUENCY SHIFT
  amplitude_ifreq : 0.2 # amplitude use to displace the imaginary frequencies to fix during analysis

  # (9) NUMBER OF MOLECULES, for eg., molecule list, for later can use as total no. of molecules it is need in the boltz part to read in specific molecules"
  maxnumber : 100000 # max number of molecules to use
