#!/usr/bin/python
from __future__ import print_function, absolute_import

#######################################################################
# Runs crest on an xyz file, can add in options to the code if needed #
#######################################################################

#Python Libraries
import sys, os
import numpy as np
from glob import glob
from optparse import OptionParser
import subprocess

def crest_opt(xyzin, xyzoutall, xyzoutbest, charge, mult, cregen, cregen_ethr, cregen_rthr, cregen_bthr,cregen_ewin):
	''' run xtb using shell script and args
	Parameters
	----------
	xyzin : str
		XYZ file for xTB optimization
	xyzoutall : str
		All conformers - Output file after xTB optimization
	xyzoutbest : str
		Best conformer - Output file after xTB optimization
	charge : int
		Total charge
	cregen : Bool
		True or False to do cregen
	cregen_ethr : float
		Energy threshold for cregen
	cregen_rthr : float
		RMS threshold for cregen
	cregen_bthr : float
		rotational constant threshold for cregen
	cregen_ewin : float
		energy window for cregen after crest
	Returns
	-------
	performs crest/cregen conformer search
	'''

	# check whether job has already been run
	if os.path.exists(xyzoutall):
		print('   {0} already exists: skipping crest search'.format(xyzoutall))
		# pass
	else:
		print('here')
		command = ['./run_crest.sh', xyzin, '--xyzoutall', str(xyzoutall),'--xyzoutbest', str(xyzoutbest), '--charge', str(charge)]
		crest_result = subprocess.run(command)

	if cregen:
		xyzcregenensemble = xyzoutall.split('.xyz')[0]+'_cregen.xyz'
		xyzcregenbest = xyzoutbest.split('.xyz')[0]+'_cregen.xyz'

		# check whether job has already been run
		if os.path.exists(xyzcregenensemble):
			print('   {0} already exists: skipping cregen search'.format(xyzcregenensemble))
			# pass
		else:
			command = ['./run_cregen.sh', xyzoutall, xyzoutbest, '--xyzout', str(xyzcregenensemble), '--charge', str(charge),'--ethr', str(cregen_ethr),'--rthr', str(cregen_rthr),'--bthr', str(cregen_bthr),'--ewin', str(cregen_ewin)]
			cregen_result = subprocess.run(command)

			#converting multiple xyz to single
			command_run_1 = ['obabel', xyzcregenensemble, '-oxyz', '-O'+xyzcregenbest,'-l','1']
			subprocess.run(command_run_1)

def main():
	# get command line inputs. Use -h to list all possible arguments and default values
	parser = OptionParser(usage="Usage: %prog [options] <input1>.xyz <input2>.xyz ...")
	parser.add_option("--charge", dest="charge", action="store", help="charge for the molecule", default=0)
	parser.add_option("--mult", dest="mult", action="store", help="Multiplicity for the molecule", default=0)

	parser.add_option("--cregen", dest="cregen", action="store_true", help="Do cregen after crest", default=False)
	parser.add_option("--cregen_ethr", dest="cregen_ethr", action="store", default=0.2, help="Energy thershold for CREGEN after crest")
	parser.add_option("--cregen_rthr", dest="cregen_rthr", action="store", default=0.125, help="RMS thershold for CREGEN fter crest")
	parser.add_option("--cregen_bthr", dest="cregen_bthr", action="store", default=0.01, help="Rotational constant thershold for CREGEN after crest")
	parser.add_option("--cregen_ewin", dest="cregen_ewin", action="store", default=6, help="Energy window for CREGEN after crest")

	(options, args) = parser.parse_args()

	files = []
	if len(sys.argv) > 1:
	  for elem in sys.argv[1:]:
		  try:
			  if os.path.splitext(elem)[1] in [".out", ".log", ".xyz"]:
				  for file in glob(elem): files.append(file)
		  except IndexError:
			  pass

	for file in files:
		name = file.split('.xyz')[0]
		outall = name+'_conformers.xyz'
		outbest = name+'_best.xyz'
		crest_opt(file, outall, outbest, options.charge, options.mult, options.cregen, options.cregen_ethr, options.cregen_rthr, options.cregen_bthr,options.cregen_ewin)

if __name__ == "__main__":
	main()
