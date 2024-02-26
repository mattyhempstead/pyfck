import random
import matplotlib.pyplot as plt
from pyfck import encode_program

random.seed(0)

def get_encoded_program_length(n):
    """
        Returns the length of an encoded program of length n.
    """

    # Generate random string
    # Technically all of unicode is supported, but a restricted charset is a good enough approximation
    available_chars = [chr(i) for i in range(0, 127)]
    random_program_string = ''.join(random.choice(available_chars) for _ in range(n))

    encoded_program = encode_program(random_program_string)
    return len(encoded_program)


# Generate the series of integers for x from 1 to 100
x_values = range(1, 101)
y_values = [get_encoded_program_length(x) for x in x_values]

print("Approximate gradient:", y_values[-1] / x_values[-1])


# Plotting
plt.ylim(bottom=0, top=max(y_values)*1.05)
plt.plot(x_values, y_values, marker='o')  # Use marker='o' for circular markers on each point

# Adding title and labels
plt.title('Growth rate of restricted charset program lengths')
plt.xlabel('Length of original program (128 charset)')
plt.ylabel('Length of restricted program (8 charset)')

# Show the plot
plt.show()
