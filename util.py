import csv
import json


def get_dictionary_list_from_file(path):
    dictionaries = []
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dictionaries.append(row)
    return dictionaries


def write_dictionary_list_to_file(dictionaries, path, data_header):
    f = open(path, "w")
    writer = csv.DictWriter(f, data_header)
    writer.writeheader()
    for dictionary in dictionaries:
        writer.writerow(dictionary)
    f.close()


def get_latest_ids_from_file(path):
    latest_ids = {}
    with open(path, 'r') as file:
        latest_ids_json = file.read()
        latest_ids = json.loads(latest_ids_json)
    return latest_ids


def get_latest_id(parameter, path):
    latest_ids = get_latest_ids_from_file(path)
    searched_id = latest_ids[parameter]
    generate_new_id(parameter, latest_ids, path)
    return searched_id


def generate_new_id(parameter, latest_ids, path):
    latest_ids[parameter] = latest_ids.get(parameter, 0) + 1
    save_latest_ids_to_file(latest_ids, path)


def find_object_by_id(parameter_id, objects):
    return object


def add_modifications_to_object(object, modifications):
    return None


def save_latest_ids_to_file(latest_ids, path):
    with open(path, 'w') as file:
        file.write(json.dumps(latest_ids))