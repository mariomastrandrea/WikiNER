import json
from urllib.request import urlopen
from src.utilities import print_percentage, csv_escape, print_line, open_files, print_count

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
labels_p  = "props=labels"
languages = "languages=en"
jformat   = "format=json"


def top_N_NEs(input_csv_ranking_file_path, output_csv_file_path, top_N=1000, aliases=False):
    """
    It labels the specified number of NERs in the input file, and writes the result in a csv file
    :param input_csv_ranking_file_path: input csv file containing the NERs IDs. It has to be a table
                                        with a header, and first column NER ID in the format Qxxxx
    :param output_csv_file_path: output csv file where to write the result. It will be a table with the same
                                format of the input file, but with an extra column containing the *label*
    :param top_N: number of top lines to be processed in the input file (default: 1000)
    :param aliases: specify if also aliases have to be retrieved or not
    """
    # 1 - open input file and output file
    files = open_files(input_csv_ranking_file_path, output_csv_file_path)
    if files is None:
        exit()  # error
    else:
        input_file, output_file = files

    # 2 - create output file from input csv
    create_labeled_csv(input_file, output_file, top_N, aliases)

    # 3 - release resources
    input_file.close()
    output_file.flush()
    output_file.close()


def create_labeled_csv(input_file, output_file, num_entries, aliases=False):
    """
    Internal method - it really labels the input file's content and write the result in the output file
    :param input_file: *opened* input file's handler
    :param output_file: *opened* output file's handler
    :param num_entries: num of top lines to be labelled
    :param aliases: specify if also the aliases have to be retrieved (True) or not (False) [default: no]
    """
    # create the new header line and write it
    new_header = f"#,{input_file.readline().strip()},Label\n"
    output_file.write(new_header)

    # Read input file and for each line extract attributes and do a http request
    #       -> save result in the output file line by line
    # (stop until the provided num of entries is reached)

    skipped_entities = []

    for i in range(num_entries):
        curr_line = input_file.readline().strip()
        entity_id = curr_line.split(sep=",")[0]     # retrieve the Qxxxx id
        rank = curr_line.split(sep=",")[1]          # retrieve the entity rank

        json_entity = get_json_entity(entity_id, aliases)    # do HTTP request to get the json representation object
        labels = json_entity["entities"][entity_id]["labels"]

        if aliases:
            aliases_entities = json_entity["entities"][entity_id]["aliases"]

        # skip entities without 'en' label
        if "en" not in labels:
            skipped_entities.append(i)
            continue

        entity_label = labels["en"]["value"]

        # write the new labeled line on the output file
        new_labeled_line = print_line(i+1, entity_id, rank, csv_escape(entity_label))
        output_file.write(new_labeled_line)

        if aliases:
            if "en" not in aliases_entities:
                continue    # no aliases

            # write eventual aliases lines
            for alias in aliases_entities["en"]:
                alias_label = alias["value"]
                alias_labeled_line = print_line(i+1, entity_id, rank, csv_escape(alias_label))
                # write the alias line on the output file
                output_file.write(alias_labeled_line)

        print_percentage(i+1, num_entries)

    print()     # newline
    if len(skipped_entities) > 0:
        print("Skipped entities:")
        print("\n".join(str(x) for x in skipped_entities))

    return


def get_json_entity(entity_id, aliases=False):
    """
    It makes an HTTPS GET request to the proper API to get the entity's information
    :param entity_id: ID of the requested entity (format: 'Qxxxx')
    :return: a dictionary with the deserialized json object (key-value pairs)
    :param aliases: specify if also the aliases have to be retrieved (True) or not (False) [default: no]
    """
    props = f"{labels_p}|aliases" if aliases else labels_p
    response = urlopen(f"https://{wiki_url}?{action}&ids={entity_id}&{languages}&{jformat}&{props}")
    json_string = response.read()        # deserialize json string
    return json.loads(json_string)       # return json object


"""
    * task3 below *
"""


def top_N_NEs_strings(input_csv_ranking_file_path, top_N=1000, aliases=False):
    """
    It labels the specified number of NERs in the input file, and save the resulting string labels in a list
    :param input_csv_ranking_file_path: input csv file containing the NERs IDs. It has to be a table
                                     with a header, and first column NER ID in the format Qxxxx
    :param top_N: number of top lines to be processed in the input file (default: 1000)
    :param aliases: specify if also the aliases have to be retrieved (True) or not (False) [default: no]
    :return: the list of the NERs labels
    """

    try:
        input_file = open(input_csv_ranking_file_path, 'r')
    except OSError:
        print("Error: specify a proper input file path")
        return False

    top_NEs = get_top_NEs_list(input_file, top_N, aliases)

    input_file.close()
    return top_NEs


def get_top_NEs_list(input_file, num_entries, aliases=False):
    """
    Internal function - it really labels the entities in the input file and return the list of strings/labels
    :param input_file: *opened* input file's handler
    :param num_entries: num of top lines to be labelled
    :param aliases: specify if also the aliases have to be retrieved (True) or not (False) [default: no]
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

        json_entity = get_json_entity(entity_id, aliases)    # do HTTP request to get the json representation
        labels = json_entity["entities"][entity_id]["labels"]

        if aliases:
            aliases_entities = json_entity["entities"][entity_id]["aliases"]

        if "en" not in labels:
            continue

        entity_label = labels["en"]["value"]

        # save the new entity_label in the output list
        output_list.append(entity_label)

        if aliases:
            if "en" not in aliases_entities:
                continue  # no aliases

            # write eventual aliases lines
            for alias in aliases_entities["en"]:
                alias_label = alias["value"]
                # save the alias label
                output_list.append(alias_label)

        print_percentage(i+1, num_entries)

    print()  # newline
    return output_list


# * label ALL the NEs - unfeasible (???) *

def save_all_NEs(input_csv_ranking_file_path, output_csv_file_path, aliases=False):
    """
    Label *all* the NEs in the input file, and writes the result in a csv file

    :param input_csv_ranking_file_path: input csv file containing the NERs IDs. It has to be a table
                                        with a header, and first column NER ID in the format Qxxxx
    :param output_csv_file_path: output csv file where to write the result. It will be a table with the same
                                format of the input file, but with an extra column containing the *label*
    :param aliases: indicate if also aliases have to be included in the result
    """
    # 1 - open input file and output file
    files = open_files(input_csv_ranking_file_path, output_csv_file_path)
    if files is None:
        exit()  # error
    else:
        input_file, output_file = files

    # 2 - create output file from input csv
    create_entire_labeled_csv(input_file, output_file, aliases)

    # 3 - release resources
    input_file.close()
    output_file.flush()
    output_file.close()


def create_entire_labeled_csv(input_file, output_file, aliases=False):
    """
    Internal method - it really labels the input file's content and write the result in the output file
    :param input_file: *opened* input file's handler
    :param output_file: *opened* output file's handler
    :param aliases: indicate if also aliases have to be included in the result
    """
    # create the new header line and write it
    new_header = f"#,{input_file.readline().strip()},Label\n"
    output_file.write(new_header)

    # Read input file and for each line extract attributes and do a http request
    #       -> save result in the output file line by line
    skipped_entities = []

    for i, line in enumerate(input_file):
        curr_line = line.strip()
        entity_id = curr_line.split(sep=",")[0]     # retrieve the Qxxxx id
        rank = curr_line.split(sep=",")[1]          # retrieve the entity rank

        json_entity = get_json_entity(entity_id, aliases)    # do HTTP request to get the json representation object
        labels = json_entity["entities"][entity_id]["labels"]

        if aliases:
            aliases_entities = json_entity["entities"][entity_id]["aliases"]

        entity_label = labels["en"]["value"]

        # skip entities without 'en' label
        if "en" not in labels:
            skipped_entities.append(i)
            continue

        # write the new labeled line on the output file
        new_labeled_line = print_line(i+1, entity_id, rank, csv_escape(entity_label))
        output_file.write(new_labeled_line)

        if aliases:
            if "en" not in aliases_entities:
                continue  # no aliases

            # write eventual aliases lines
            for alias in aliases_entities["en"]:
                alias_label = alias["value"]
                alias_labeled_line = print_line(i + 1, entity_id, rank, csv_escape(alias_label))
                # write the alias line on the output file
                output_file.write(alias_labeled_line)

        # print the number of lines (NEs) written so far
        print_count(i+1)

    print()  # newline
    if len(skipped_entities) > 0:
        print("Skipped entities:")
        print("\n".join(str(x) for x in skipped_entities))
    return


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

    # Read input file and for each line extract attributes and do a http request
    #       -> save result in the output list

    for line in input_file:
        curr_line = line.strip()
        entity_label = curr_line.split(sep=",")[3]     # retrieve the label

        # save the new entity_label in the output list
        output_list.append(entity_label[1:-1])

    return output_list

