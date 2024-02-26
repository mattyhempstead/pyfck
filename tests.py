import subprocess
from pyfck import encode_program, CHARSET
# from pyfck_old import encode_program, CHARSET

"""
    Unfortunately checking two programs are equivalent is a *little* challenging.

    So I'll just check their stdout is the same and also run some post checks.
"""


"""
    A list of programs to test.
"""
tests = [
    {
        # Variable assignment
        'program': 'c=8',
        'stdout': '',
        'stderr': '',
        'post_checks': [
            'assert(c==8)',
        ],
    },
    {
        # Printing
        'program': 'print(3)',
        'stdout': '3\n',
        'stderr': '',
        'post_checks': [],
    },
    {
        # Usage of percent symbol
        'program': 'print("%", 100 % 7)',
        'stdout': '% 2\n',
        'stderr': '',
        'post_checks': [],
    },
    {
        # Multiline program
        'program': 'c=8\nprint(3*c+1)',
        'stdout': '25\n',
        'stderr': '',
        'post_checks': [
            'assert(c==8)'
        ],
    },
    {
        # Function definition and calling
        'program': 'def f(k):\n    print(k)\nf(1)\nf(2)',
        'stdout': '1\n2\n',
        'stderr': '',
        'post_checks': [
            'assert(callable(f))'
        ],
    },
    {
        # Error case
        'program': '1/0',
        'stdout': '',
        'stderr': 'ZeroDivisionError: division by zero',
        'post_checks': [],
    }
]


def assert_program_output(program: str, expected_stdout: str, expected_stderr: str) -> bool:
    # Execute the program and capture its stdout and stderr
    result = subprocess.run(['python', '-c', program], capture_output=True, text=True)

    # Compare the captured stdout/stderr to the expected strout/stderr
    assert(result.stdout == expected_stdout), f'Expected stdout: "{expected_stdout}", but got: "{result.stdout}"'

    # Stacktrace won't be exactly the same because line numbers and code is different.
    # Instead we just check for the existence of expected error strings, which is good enough.
    assert(expected_stderr in result.stderr), f'Expected stderr to contain "{expected_stderr}", but got: "{result.stderr}"'

    return True



for test in tests:
    print("Checking", test)

    stdout = test['stdout']
    stderr = test['stderr']

    post_checks = test['post_checks']
    post_checks_string = '\n'+'\n'.join(post_checks)

    program = test['program']
    program_checked = program + post_checks_string

    program_encoded = encode_program(program)
    program_encoded_checked = program_encoded + post_checks_string

    print("Original length:", len(program))
    print("Encoded length:", len(program_encoded))

    # Check encoded program respects the limited character set
    assert(set(program_encoded) == set(CHARSET))
    print("Unique characters:", len(set(program_encoded)))

    # Check given program has expected output
    assert_program_output(program, stdout, stderr)

    # Check given program with post checks has expected output
    assert_program_output(program_checked, stdout, stderr)

    # Check encoded program has expected output
    assert_program_output(program_encoded, stdout, stderr)

    # Check encoded program with post checks has expected output
    assert_program_output(program_encoded_checked, stdout, stderr)

    print()
