"""
file containing just utility functions for other scripts
"""


def open_files(read_file, write_file):
    """
    It opens the two specified files in read mode ('r') and in write mode ('w') respectively
    :param read_file: path of the file you want to read
    :param write_file: path of the file you want to write to
    :return: file handlers of the 2 specified files, already opened
    """
    try:
        input_file = open(read_file, 'r')
    except OSError:
        print("Error: specify a proper input file path")
        return False

    try:
        output_file = open(write_file, 'w')
    except OSError:
        print("Error: specify a proper output file path")
        return False

    return input_file, output_file


def print_percentage(x, scale):
    perc = x/scale * 100
    print("\rLoading: ", end="")
    print("{:.1f}%".format(perc), end="")


def csv_escape(word):
    return f"\"{word}\""


def print_line(*fields):
    """
    It prints the specified fields in a csv-style and add a newline at the end
    """
    return ",".join((str(x) for x in fields)) + "\n"
