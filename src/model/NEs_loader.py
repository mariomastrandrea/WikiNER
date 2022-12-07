
def get_NEs_from_file(input_csv_file):
    """
    Upload Named Entities from a csv file, instead of computing them on the fly by means of an API.
    The csv file must have a header line and the (quoted) label of the NE in the 4th column
    :param input_csv_file: filepath of the csv file containing the Named Entities
    :return: a list of strings containing all the Named Entities in the file
    """
    try:
        input_file = open(input_csv_file, 'r')
    except OSError:
        print("Error: specify a proper input file path")
        return None

    output_list = list()
    input_file.readline()  # skip header line

    # Read input file and for each line extract the NE's label
    #       -> save result in the output list

    for i, line in enumerate(input_file):
        curr_line = line.strip()
        entity_label = curr_line.split(sep=",")[3]     # retrieve the (quoted) label
        entity_label = entity_label[1:-1]   # remove quotes

        # save the new entity_label in the output list
        output_list.append(entity_label)

        print("\rLine:", i+1, end="")

    print()     # newline
    return output_list
