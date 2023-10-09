## pyfck

CHARSET = ['e', 'x', 'c', '%', '(', ')', "'", '=']


encoded_True = "(''=='')"
encoded_False = "(''==())"

# encoded_0_str = f"('%x'%{encoded_True})"
# encoded_1_str = f"('%x'%{encoded_True})"

# the program "x=11"
encoded_x_equals_11: str = f"'x=%x%%x'%{encoded_True}%{encoded_True}"



def encode_format_str(char:str, length:int):
    """
        Construct "%c%%c%%%%c..." style string for formatting.
        `char` can be "x" or "c" or anything else valid in python3.

        Unfortunatley the number of % must double for every additional character.
        If someone can come up with a format method that is <O(2^n) (O(n)??) that would be great.
    """
    format_str = ""
    for i in range(length):
        format_str += "%"*(2**(i)) + char
    return format_str


def encode_digit_var(n: int) -> str:
    """
        Returns the variable name that a digit is assigned to.

        We generate var names by taking the binary representation of n
        and swapping 0 with c and 1 with e (bc c & e are with our charset).

        e.g. 123 -> 0b1111011 -> eeeecee is our variable name for the digit 123
    """
    return bin(n)[2:].replace('0','c').replace('1','e')


def encode_digit_assignment(n: int) -> str:
    """
        Encode digit with charset assuming we have x=11.

        Returns a program that when executed, will assign a variable
        with this integer value to variable name specified by encode_digit_var(n)
    """
    encoded_map = {
        "b": "x",   # '%x'%x == '%x'%11 == 'b'
        "0": encoded_False,
        "1": encoded_True,
    }

    # get string of each integer
    bin_repr = list(bin(n))
    encoded_bin_repr = [encoded_map[c] for c in bin_repr]

    # print(bin_repr)
    # print(encoded_bin_repr)

    # construct %c%%c%%%%c%... style string formatting that we can format with encoded bin repr
    encoded_format_str = encode_format_str('x', len(encoded_bin_repr))
    # print(encoded_format_str)

    encoded_digit_var = encode_digit_var(n)
    # print(encoded_digit_var)

    encoded_digit = f"'{encoded_digit_var}={encoded_format_str}'%" + "%".join(encoded_bin_repr)
    # print(encoded_digit)

    return encoded_digit



def encode_str(s: str) -> str:
    """
        Encodes an arbitrary string with the charset.

        Assumes that all required ascii integers are assigned to variables
        using the naming convention outlined in encode_digit_var().
    """
    # print(s)

    encoded_format_str = encode_format_str('c', len(s))
    # print(encoded_format_str)

    encoded_vars = [encode_digit_var(ord(c)) for c in list(s)]
    # print(encoded_vars)

    encoded_str = f"'{encoded_format_str}'%" + "%".join(encoded_vars)
    # print(encoded_str)

    return encoded_str



def encode_program(program: str) -> str:
    """
        Returns entire program encoded using charset.

        The string returned here can be executed directly by pasting in a python interpreter.
    """

    statements = []

    # Need this first to assign x=11 (gives us access to 'b' char)
    statements.append(encoded_x_equals_11)

    # Assign all unique characters in program to variables
    for c in set(program):
        statements.append(encode_digit_assignment(ord(c)))

    # Encoded program itself
    statements.append(encode_str(program))

    # for s in statements:
    #     print(s)
    # print(statements)


    encoded_program = "==".join(f"exec({s})" for s in statements)
    print(encoded_program)

    print(set(encoded_program))



# print(encoded_x_equals_11)

# encode_digit_assignment(12)

# encode_str("print(0)")
# encode_str("a=2")

# encode_program("a=2")
# encode_program("x=0\nprint(x)")


