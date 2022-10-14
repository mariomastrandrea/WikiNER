
def open_files(read_file, write_file):
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
    return ",".join((str(x) for x in fields)) + "\n"
