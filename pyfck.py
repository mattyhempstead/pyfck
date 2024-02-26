## pyfck

CHARSET = ['e', 'x', 'c', '%', '(', ')', "'", '=']


encoded_True = "(''=='')"
encoded_False = "(''==())"

# The program "x=11"
encoded_x_equals_11 = f"'x=%x%%x'%{encoded_True}%{encoded_True}"

# Executable statements to help produce O(n) program sizes
linear_asymptotic_init = "xx=''"
linear_asymptotic_append = "xx+=chr(%d)"
linear_asymptotic_exec = "xx"


def encode_format_str(char:str, length:int):
    """
        Construct "%c%%c%%%%c..." style string for formatting.
        `char` can be "x" or "c" or anything else valid in python3.

        Note the number of % must double for every additional character.
        So we shouldn't use this to encode the entire program string all at once.
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
        Uses the exponentially growing string %c%%c%%%%c... method.

        Assumes that all required ascii integers are assigned to variables
        using the naming convention outlined in encode_digit_var().

        Optionally will apply the linear_asymptotic trick which assumes
        xx(a,b)->(a+b) is defined to allow appending of strings.
    """
    # print(s)

    encoded_vars = [encode_digit_var(ord(c)) for c in list(s)]
    # print(encoded_vars)

    encoded_format_str = encode_format_str('c', len(s))
    # print(encoded_format_str)

    encoded_str = f"'{encoded_format_str}'%" + "%".join(encoded_vars)
    # print(encoded_str)

    return encoded_str



def encode_program(program: str, linear_asymptotic: bool = False) -> str:
    """
        Returns entire program encoded using charset.

        The string returned here can be executed directly by pasting in a python interpreter.
    """
    # Don't use the linear asymptotic trick if it won't help
    # linear_asymptotic &= len(program) >= len(encoded_linear_asymptotic_program)

    statements = []

    # Need this first to assign x=11 (gives us access to 'b' char)
    statements.append(encoded_x_equals_11)


    # Generate a list of statements which assign all unique characters we need to variables
    chars = set(program)
    chars |= set(linear_asymptotic_init)

    for c in program:
        chars |= set(linear_asymptotic_append % ord(c))

    for c in sorted(chars):# + linear_asymptotic*set(encoded_linear_asymptotic_program):
        statements.append(encode_digit_assignment(ord(c)))


    # Note the below statements using xx can probably be reduced in size
    # by substituting the characters we already have access to (e.g. xx=)
    # with their actual characters rather than re-encoding them.

    # Execute xx=''
    statements.append(encode_str(linear_asymptotic_init))

    # Execute xx+=chr(n) for all characters c where n=ord(c)
    # e.g. xx+=chr(100) will append 'd' to xx
    for c in program:
        statements.append(encode_str(linear_asymptotic_append % ord(c)))

    # Execute xx, which should be a string containing the original program
    statements.append(linear_asymptotic_exec)

    # Encoded program itself
    # statements.append(encode_str(program))

    # for s in statements:
    #     print(s)
    # print(statements)

    encoded_program = "==".join(f"exec({s})" for s in statements)
    # print(encoded_program)

    return encoded_program



if __name__ == '__main__':

    # program = "c=8"
    # program = 'print("Hello World!")'
    program = "x=5\nprint(x)"

    encoded_program = encode_program(program)

    print(encoded_program)

    print(set(encoded_program))

    print(len(program), len(encoded_program))
