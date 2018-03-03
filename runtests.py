#
#  THIS DOES NOT WORK YET
#
import os, os.path, subprocess

def compile_a_test(filename, bc_file):
    """
    Compiles the given file using sparse-llvm and saves output to the
    bc_file; bc_file will be created
    :param filename: The C source file to be compiled
    :param bc_file: The file that will be generated after compilation
    :return: True on success
    """
    if os.path.isfile(bc_file):
        os.remove(bc_file)
    with open(bc_file, "wb") as f:
        result = subprocess.run(['sparse-llvm', filename], stdout=f,
                            stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return True
    return False

def get_expected_output(filename):
    """
    Returns the expected output from a test as a string.
    The expected output for program.c is looked in program.expect.
    If no expected output is available returns None
    :param filename: The C source file name
    :return: Expected output after running the test
    """
    (basename, ext) = os.path.splitext(filename)
    expected_output_file = basename + '.expect'
    expected_output = None
    if os.path.isfile(expected_output_file):
        with open(expected_output_file) as f:
            expected_output = f.read()
    return expected_output

def execute_test(bc_file):
    """
    Executes the given LLVM bitcode file using lli
    and returns a tuple indicating whether the program
    terminated normally and any output from the program
    :param bc_file: The LLVM bitcode file to execute
    :return: Tuple pair - status and output
    """
    result = subprocess.run(['lli', bc_file], universal_newlines=True, stdout=subprocess.PIPE)
    if result.returncode != 0:
        return False, None
    return True, result.stdout


def run_a_test(filename, results_directory):
    bc_file = os.path.join(results_directory, 'out.bc')
    if not compile_a_test(filename, bc_file):
        print('Test ' + filename + ' FAILED to compile')
        return False
    (status, actual_output) = execute_test(bc_file)
    if not status:
        print('Test ' + filename + ' FAILED (non-zero code)')
        return False
    expected_output = get_expected_output(filename)
    if expected_output and expected_output != actual_output:
        print('Test ' + filename + ' FAILED (output mismatch)')
        # print('Expected -->')
        # print(expected_output)
        # print('Actual -->')
        # print(actual_output)
        return False
    print('Test ' + filename + ' OK')
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
