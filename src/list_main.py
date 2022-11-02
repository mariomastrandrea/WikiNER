import sys

from src.model.preprocesser import top_N_NEs_strings

"""
This main file runs a program capable of processing a csv input (NERs IDs)
and prints the output (tagged NERs) on the *console* (stdout)
"""


def check_and_return_inputs():
    # (2nd argument - [num entries] - is optional)
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: csv_main.py <input file> [num entries]")
        return None

    input_path = sys.argv[1]

    if len(sys.argv) == 2:
        return [input_path]

    elif len(sys.argv) == 3:
        try:
            entries = int(sys.argv[2])
        except ValueError:
            print("Error: the second argument must be an integer number")
            return None

        return [input_path, entries]


if __name__ == '__main__':
    # check and retrieve input parameters values: input file path, output file path (, number of entries)
    inputs = check_and_return_inputs()
    if inputs is None:  # input error
        exit()

    # no num_entries specified (use default one)
    if len(inputs) == 1:
        (input_file_path) = inputs
        NEs = top_N_NEs_strings(input_file_path)
    # user specified num_entries
    elif len(inputs) == 2:
        input_file_path, num_entries = inputs
        NEs = top_N_NEs_strings(input_file_path, num_entries)


    # print results on stdout: one entity per line
    print()  # newline
    print('\n'.join(NEs))
