import os
from pprint import pprint
import json
import datetime
import tkinter as tk
import time
iso_date = datetime.date.today().isoformat()

DATABASE = "highlights_notes.json"
INBOX = "/Users/liam/Desktop/bookmarker/highlights_notes_inbox/"


def read_bookmarks_highlights_json():
    """Reads the bookmakrks JSON and returns a python dict."""
    with open(DATABASE, 'r') as highlights_and_notes:
        highlights_and_notes = highlights_and_notes.read()

        #print(f"{highlights_and_notes = }")
        #print(type(highlights_and_notes))

        my_dict = json.loads(highlights_and_notes)
        return my_dict

def read_input_files(filepaths: list):
    
    def strip_items_of_whitespace(x: dict):
        for key in x.keys():
            if type(x[key]) == str:
                x[key] = x[key].strip()
        return x

    entries_to_add_to_database = []

    for filepath in filepaths:


        with open(INBOX + filepath, 'r') as input:
            new_entry = input.read()
            my_dict = json.loads(new_entry)
            my_dict["entry"] = strip_items_of_whitespace(my_dict["entry"])
            my_dict = strip_items_of_whitespace(my_dict)
            entries_to_add_to_database.append(my_dict)
    
    return entries_to_add_to_database



def find_new_files():
    """Will check for new new files using os.listdir()"""

    files = os.listdir(INBOX)
    txt_files = [file for file in files if file.endswith('.txt')]

    checked_files = []

    for txt_file in txt_files:
        try:
            json.loads(txt_file)
        except:
            checked_files.append(txt_file)

    return txt_files

def delete_leftovers():
    """filepaths_to_delete = find_new_files()
    for filepath in filepaths_to_delete:
        os.remove(f"{INBOX + filepath}")"""
    filepaths_to_delete = find_new_files()
    for filepath in filepaths_to_delete:
        os.remove(f"{INBOX + filepath}")

def create_new_json_object(original_object: dict, new_entries: list) -> str:
    """database_to_return = original_object
    
    for entry in new_entries:
        if entry["entry"]["is_highlight"]:
            database_to_return["highlights"].append(entry["entry"])
    database_to_return = json.dumps(database_to_return)

    return database_to_return"""
    
    database_to_return = original_object
    
    for entry in new_entries:
        if entry["entry"]["is_highlight"]:
            database_to_return["highlights"].append(entry["entry"])
    database_to_return = json.dumps(database_to_return)

    return database_to_return

def write_new_highlights_json(thing_to_replace_database_with: str) -> None:
    """Receives a new json string, and replaces the original."""
    with open(DATABASE, "w") as highlights_and_notes:
        highlights_and_notes.write(thing_to_replace_database_with)

def backup_database(unique_ref: str, db_to_backup: str):
    with open("backups/highlights_notes" + f" {unique_ref}.json", "w") as highlights_and_notes:
        highlights_and_notes.write(db_to_backup)

def create_list_of_attributes(entries: list, attribute_to_make_list_of: str):
    "Scans entries for list of authors, removes duplicates"

    unique_attributes = set([attribute[attribute_to_make_list_of] for attribute in entries])
    unique_attributes = "\n".join(unique_attributes)

    with open(attribute_to_make_list_of + ".txt", "w") as out_file:
        out_file.write(unique_attributes)
    
    return unique_attributes




"""BRAINWAVE

Notes should not be a separate entry in the dictionary, as they will always be attributed to a highlight.
Each attribute should have a note key, which will simply be a list."""


def sweep_for_new_files_and_cleanup():
    """Shouldn't be called externally."""
    
    new_files = find_new_files()
    entries = read_input_files(new_files)
    original_database = read_bookmarks_highlights_json()
    new_database = create_new_json_object(original_database, entries)
    new_database_as_dict = json.loads(new_database)
    create_list_of_attributes(new_database_as_dict["highlights"], "author")
    create_list_of_attributes(new_database_as_dict["highlights"], "title")
    backup_database(unique_ref = iso_date, db_to_backup = new_database)
    write_new_highlights_json(new_database)
    delete_leftovers()


"""Need to do some kind of whitespace clearing at the end of strings for author names as well"""

if __name__ == "__main__":
    start_time = time.perf_counter()
    sweep_for_new_files_and_cleanup()
    end_time = time.perf_counter()
    
    time_elapsed = round(
        (end_time-start_time)*1000,
        2
        )
    
    print(f'Time elapsed: {time_elapsed}ms')
    print(iso_date)