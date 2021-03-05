""" 
IO Test Implementation
"""
import subprocess
from difflib import ndiff
import os

test_dir = './tests'
program = './main'
tests_files = os.listdir(test_dir)

if len(tests_files) == 0:
  print("No test found.")
  quit()

if not os.path.isfile(program):
  print(f"Program {program} not found.")
  quit()

input_files = filter(lambda s : s.endswith('.in'), tests_files)
output_files = filter(lambda s : s.endswith('.expect'), tests_files)

tasks = {} 

for in_file in input_files:
  taskname = in_file[:-3]
  if not (taskname + '.expect') in output_files:
    print(f"No expect file for {taskname}.expect.")
    quit()
  tasks[taskname] = (in_file, taskname + '.expect')


def compare_output(output: str, expect: str, error: str):
  """ Compares the output of the program
  Args:
      output (str): program output
      expect (str): expected output
      error (str):  program stdout
  """
  if output == expect:
    print("Test Passed.")
  else:
    print("Task failed.")
    print('=' * 10, end='')
    print(' Output Differences ', end='')
    print('=' * 10)
    
    # output the difference
    diff = ndiff(output.splitlines(keepends=True),
                 expect.splitlines(keepends=True))
    print(''.join(diff), end='')

    print('=' * 40)
    print("Program stdout: ")
    print(output)
    print('-' * 40)
    print("Expected result: ")
    print(expect)
    print('=' * 40)
    print("program stderr: ")
    print(error)
    

for task, files in tasks.items():
  inf, expectf = files
  with open(f"{test_dir}/{inf}", 'r') as input_stream:
    # Print task information
    print('-' * 10, end='')
    print(f" Running task ({task}) ", end='')
    print('-' * 10)
    # Run the process
    try:
      proc = subprocess.run(program, stdin=input_stream, 
                            timeout=3, capture_output=True)

      output = proc.stdout.decode("utf-8")
      errors = proc.stderr.decode("utf-8")
      
      if proc.returncode != 0:
        print(f"Process return with non-zero exit code {proc.returncode}.")
        print("stderr: ")
        print(errors)
        print("stdout: ")
        print(output)
        continue
      
      with open(f"{test_dir}/{expectf}", 'r') as expect:
        expected_result = expect.read()
        compare_output(output, expected_result, errors)

    except subprocess.TimeoutExpired:
      print("Process timed out.")
      print(proc.stdout.decode("utf-8"))
      print(proc.stderr.decode("utf-8"))
    


