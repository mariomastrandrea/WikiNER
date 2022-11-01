import json
from urllib.request import urlopen
from utilities import print_percentage, csv_escape, print_line, open_files

wiki_url  = "www.wikidata.org/w/api.php"
action    = "action=wbgetentities"
props     = "props=labels"
languages = "languages=en"
jformat   = "format=json"

# * task1 *


def top_N_NEs(input_csv_ranking_file_path, output_csv_file_path, top_N=1000):
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

        json_entity = get_json_entity(entity_id)    # do HTTP request to get the json representation
        entity = json.loads(json_entity)            # deserialize json string
        entity_label = entity["entities"][entity_id]["labels"]["en"]["value"]

        # write the new labeled line on the output file
        new_labeled_line = print_line(i+1, entity_id, rank, csv_escape(entity_label))
        output_file.write(new_labeled_line)

        print_percentage(i+1, num_entries)

    print()     # newline
    return


def get_json_entity(entity_id):
    response = urlopen(f"https://{wiki_url}?{action}&{props}&ids={entity_id}&{languages}&{jformat}")
    return response.read()


# * task3 *


def top_N_NEs_strings(input_csv_ranking_file_path, top_N=1000):
    try:
        input_file = open(input_csv_ranking_file_path, 'r')
    except OSError:
        print("Error: specify a proper input file path")
        return False

    top_NEs = get_top_NEs_list(input_file, top_N)

    input_file.close();
    return top_NEs


def get_top_NEs_list(input_file, num_entries):
    output_list = list()
    input_file.readline();  # skip header line

    # Read input file and for each line extract attributes and do a http request
    #       -> save result in the output list
    # (stop until the provided num of entries is reached)

    for i in range(num_entries):
        curr_line = input_file.readline().strip()
        entity_id = curr_line.split(sep=",")[0]     # retrieve the Qxxxx id

        json_entity = get_json_entity(entity_id)    # do HTTP request to get the json representation
        entity = json.loads(json_entity)            # deserialize json string into dict
        entity_label = entity["entities"][entity_id]["labels"]["en"]["value"]

        # save the new entity_label in the output list
        output_list.append(entity_label)

        print_percentage(i+1, num_entries)

    print()  # newline
    return output_list



