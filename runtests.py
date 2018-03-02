#
#  THIS DOES NOT WORK YET
#


import os, os.path, subprocess

def run_tests(test_directory, results_directory):
	os.chdir(test_directory)
	print('Running tests in ' + test_directory)
	with os.scandir(test_directory) as it:
		for entry in it:
			if not entry.name.endswith('.c') or not entry.is_file():
				continue
			print('Running test ' + entry.name)
			(basename, ext) = os.path.splitext(entry.name)
			print('  Basename ' + basename)
			expected_output_file = basename + '.expect'
			expected_output = None
			if os.path.isfile(expected_output_file):
				with open(expected_output_file) as f:
					expected_output = f.read()


current_directory = os.getcwd()
temp_directory = os.path.join(current_directory, 'test_results')
print('Using folder [' + temp_directory + '] for test results') 


with os.scandir(current_directory) as it:
	for entry in it:
		if not entry.name.startswith('.') and entry.is_dir():
			print('Running tests in ' + entry.name)
			run_tests(entry.path, temp_directory)




