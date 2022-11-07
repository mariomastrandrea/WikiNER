# usage: csv_main.py <input file> <output file> [num entries]
import sys
import time

from src.model.preprocesser import top_N_NEs, save_all_NEs

"""
This main file runs a program capable of processing a csv input (NERs IDs)
and writes the output (tagged NERs) in another *csv file* 
"""


def check_and_return_csv_inputs():
    # (3rd argument - [num entries] - is optional)
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: csv_main.py <input file> <output file> [num entries]")
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

        return [input_path, output_path, entries]


if __name__ == '__main__':
    # check and retrieve input parameters values: input file path, output file path (, number of entries)
    inputs = check_and_return_csv_inputs()
    if inputs is None:  # input error
        exit()

    # now compute the top N Named Entities from input csv and write them to output csv

    # measure elapsed time: start
    eff_start_time = time.process_time()
    start_time = time.time()

    # no num_entries specified (use default one)
    if len(inputs) == 2:
        input_file_path, output_file_path = inputs
        top_N_NEs(input_file_path, output_file_path)
    # user specified num_entries
    elif len(inputs) == 3:
        input_file_path, output_file_path, num_entries = inputs
        top_N_NEs(input_file_path, output_file_path, num_entries)

    # measure elapsed time: end
    eff_end_time = time.process_time()
    end_time = time.time()

    eff_elapsed_time = eff_end_time - eff_start_time
    elapsed_time = end_time - start_time

    print(f"Effective elapsed time: {int(eff_elapsed_time)} seconds")
    print(f"Elapsed time: {int(elapsed_time)} seconds")



"""
main function for computing all the NEs - unfeasible (???) 

def check_and_return_csv_inputs_for_all_NEs():
    if len(sys.argv) != 3:
        print("Usage: csv_main.py <input file> <output file>")
        return None

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    return [input_path, output_path]



if __name__ == '__main__':
    # check and retrieve input parameters values: input file path, output file path
    inputs = check_and_return_csv_inputs_for_all_NEs()
    if inputs is None:  # input error
        exit()

    # now take *all* the Named Entities from input csv and write them to output csv

    input_file_path, output_file_path = inputs
    save_all_NEs(input_file_path, output_file_path)
"""
