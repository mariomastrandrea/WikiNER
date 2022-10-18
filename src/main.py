# usage: main.py <input file> <output file> [num entries]
import sys
from preprocesser import top_N_NEs


def check_and_return_inputs():
    # (3rd argument - [num entries] - is optional)
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: main.py <input file> <output file> [num entries]")
        return None

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if len(sys.argv) == 3:
        return [input_path, output_path]

    elif len(sys.argv) == 4:
        try:
            entries = int(sys.argv[3])
        except ValueError:
            print("Error: the third argument must be an integer number")
            return None
        fgv

        return [input_path, output_path, entries]


if __name__ == '__main__':
    # check and retrieve input parameters values: input file path, output file path (, number of entries)
    inputs = check_and_return_inputs()
    if inputs is None:  # input error
        exit()

    # now compute the top N Named Entities from input csv and write them to output csv

    # no num_entries specified (use default one)
    if len(inputs) == 2:
        input_file_path, output_file_path = inputs
        top_N_NEs(input_file_path, output_file_path)
    # user specified num_entries
    elif len(inputs) == 3:
        input_file_path, output_file_path, num_entries = inputs
        top_N_NEs(input_file_path, output_file_path, num_entries)
