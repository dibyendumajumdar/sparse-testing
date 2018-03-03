#
#  THIS DOES NOT WORK YET
#
import os, os.path, subprocess

def run_a_test(filename, results_directory):
	print('Running test ' + filename)
	(basename, ext) = os.path.splitext(filename)
	expected_output_file = basename + '.expect'
	expected_output = None
	bc_file = os.path.join(results_directory, 'out.bc')
	if os.path.isfile(expected_output_file):
		with open(expected_output_file) as f:
			expected_output = f.read() 
	if (os.path.isfile(bc_file)):
		os.remove(bc_file)
	result = subprocess.run(['sparse-llvm', filename, '-o', bc_file], stdout=subprocess.DEVNULL, 
		stderr=subprocess.STDOUT)
	if result.returncode != 0:
		print('Test ' + filename + ' FAILED to compile')
		return False
	result = subprocess.run(['lli', bc_file], universal_newlines=True, stdout=subprocess.PIPE)
	if result.returncode != 0:
		print('Test ' + filename + ' FAILED (non-zero code)')
		return False
	actual_output = result.stdout
	if expected_output != None and expected_output != actual_output:
		print('Test ' + filename + ' FAILED (output mismatch)')
		#print('Expected -->')
		#print(expected_output)
		#print('Actual -->')
		#print(actual_output)
		return False
	return True		

def run_tests(test_directory, results_directory):
	# We CD to the location where the sources are as some tests
	# include other files
	os.chdir(test_directory)
	print('Running tests in ' + test_directory)
	with os.scandir(test_directory) as it:
		for entry in it:
			if not entry.name.endswith('.c') or not entry.is_file():
				continue
			run_a_test(entry.path, results_directory)

current_directory = os.getcwd()

# The compiled output will be generated in test_results folder (out.bc)
temp_directory = os.path.join(current_directory, 'test_results')
if not os.path.isdir(temp_directory):
	os.mkdir(temp_directory)
print('Using folder [' + temp_directory + '] for test results') 

with os.scandir(current_directory) as it:
	for entry in it:
		if not entry.name.startswith('.') and entry.is_dir():
			run_tests(entry.path, temp_directory)




