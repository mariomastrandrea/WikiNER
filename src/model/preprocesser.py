import json
from urllib.request import urlopen
from src.utilities import print_percentage, csv_escape, print_line, open_files

"""
This file contains the main functions for processing input NEs IDs, labelling them and 
returning the result in a proper output format (csv, list of strings, etc.) 
"""


"""
    * task1 below *
"""

# useful string parameters
wiki_url  = "www.wikidata.org/w/api.php"
action    = "action=wbgetentities"
props     = "props=labels"
languages = "languages=en"
jformat   = "format=json"


def top_N_NEs(input_csv_ranking_file_path, output_csv_file_path, top_N=1000):
    """
    It labels the specified number of NERs in the input file, and writes the result in a csv file
    :param input_csv_ranking_file_path: input csv file containing the NERs IDs. It has to be a table
                                        with a header, and first column NER ID in the format Qxxxx
    :param output_csv_file_path: output csv file where to write the result. It will be a table with the same
                                format of the input file, but with an extra column containing the *label*
    :param top_N: number of top lines to be processed in the input file (default: 1000)
    """
    # 1 - open input file and output file
    files = open_files(input_csv_ranking_file_path, output_csv_file_path)
    if files is None:
        exit()  # error
    else:
        input_file, output_file = files

    # 2 - create output file from input csv
    create_labeled_csv(input_file, output_file, top_N)

    # 3 - release resources
    input_file.close()
    output_file.flush()
    output_file.close()


def create_labeled_csv(input_file, output_file, num_entries):
    """
    Internal method - it really labels the input file's content and write the result in the output file
    :param input_file: *opened* input file's handler
    :param output_file: *opened* output file's handler
    :param num_entries: num of top lines to be labelled
    """
    # create the new header line and write it
    new_header = f"#,{input_file.readline().strip()},Label\n"
    output_file.write(new_header)

    # Read input file and for each line extract attributes and do a http request
    #       -> save result in the output file line by line
    # (stop until the provided num of entries is reached)

    for i in range(num_entries):
        curr_line = input_file.readline().strip()
        entity_id = curr_line.split(sep=",")[0]     # retrieve the Qxxxx id
        rank = curr_line.split(sep=",")[1]          # retrieve the entity rank

        json_entity = get_json_entity(entity_id)    # do HTTP request to get the json representation object
        entity_label = json_entity["entities"][entity_id]["labels"]["en"]["value"]

        # write the new labeled line on the output file
        new_labeled_line = print_line(i+1, entity_id, rank, csv_escape(entity_label))
        output_file.write(new_labeled_line)

        print_percentage(i+1, num_entries)

    print()     # newline
    return


def get_json_entity(entity_id):
    """
    It makes an HTTPS GET request to the proper API to get the entity's information
    :param entity_id: ID of the requested entity (format: 'Qxxxx')
    :return: a dictionary with the deserialized json object (key-value pairs)
    """
    response = urlopen(f"https://{wiki_url}?{action}&{props}&ids={entity_id}&{languages}&{jformat}")
    json_string = response.read()        # deserialize json string
    return json.loads(json_string)       # return json object


"""
    * task3 below *
"""


def top_N_NEs_strings(input_csv_ranking_file_path, top_N=1000):
    """
    It labels the specified number of NERs in the input file, and save the resulting string labels in a list
    :param input_csv_ranking_file_path: input csv file containing the NERs IDs. It has to be a table
                                     with a header, and first column NER ID in the format Qxxxx
    :param top_N: number of top lines to be processed in the input file (default: 1000)
    :return: the list of the NERs labels
    """

    try:
        input_file = open(input_csv_ranking_file_path, 'r')
    except OSError:
        print("Error: specify a proper input file path")
        return False

    top_NEs = get_top_NEs_list(input_file, top_N)

    input_file.close()
    return top_NEs


def get_top_NEs_list(input_file, num_entries):
    """
    Internal function - it really labels the entities in the input file and return the list of strings/labels
    :param input_file: *opened* input file's handler
    :param num_entries: num of top lines to be labelled
    :return: the list of the desired labels
    """
    output_list = list()
    input_file.readline()  # skip header line

    # Read input file and for each line extract attributes and do a http request
    #       -> save result in the output list
    # (stop until the provided num of entries is reached)

    for i in range(num_entries):
        curr_line = input_file.readline().strip()
        entity_id = curr_line.split(sep=",")[0]     # retrieve the Qxxxx id

        json_entity = get_json_entity(entity_id)    # do HTTP request to get the json representation
        entity_label = json_entity["entities"][entity_id]["labels"]["en"]["value"]

        # save the new entity_label in the output list
        output_list.append(entity_label)

        print_percentage(i+1, num_entries)

    print()  # newline
    return output_list


