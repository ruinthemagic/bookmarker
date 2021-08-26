import os
from pprint import pprint
import json
import sweep_for_new_files_and_cleanup as utilities
from edit_entry_gui import get_new_text_from_user_gui


DATABASE = utilities.read_bookmarks_highlights_json()

def search_by_clipping(search_term: str = '') -> list:

    if not search_term:
        search_term = input('Enter a search term: ')
    
    entries = [(entry, str(DATABASE["highlights"].index(entry))) for entry in DATABASE["highlights"] if search_term in entry["clipping"]]

    formatted_entries = ""

    for entry in entries:
        id = entry[1]
        entry = entry[0]
        entry_to_append = entry_formatter(
            author=entry["author"],
            title=entry["title"],
            clipping=entry["clipping"],
            timestamp=entry["timestamp"],
            id = id
            )

        formatted_entries = formatted_entries + entry_to_append + "\n"
    print(formatted_entries)

    return entries

def search_by_id(id = None):
    if not id:
        id = int(input('Please enter an ID: '))
    # print(DATABASE["highlights"][id])
    print(entry_formatter_for_full_entry(DATABASE["highlights"][id]))
    return DATABASE["highlights"][id]    

def delete_entries(db: dict = {}, entries_to_delete = None):
    if not db:
        db = utilities.read_bookmarks_highlights_json()
    if not entries_to_delete:
        entries_to_delete = search_by_clipping()


    new_db = db
    for entry in entries_to_delete:
        if entry in new_db["highlights"]:
            new_db["highlights"].remove(entry)
    
    utilities.write_new_highlights_json(json.dumps(new_db))

    return new_db

def replace_entry(item_to_replace, new_item):
    """Takes two entries. Searches for the first, and replaces it with the second."""
    db_copy = DATABASE

    highlights = db_copy["highlights"]
    for count, item in enumerate(highlights):
        if item == item_to_replace:
            highlights[count] = new_item
    
    db_copy["highlights"] = highlights

    utilities.write_new_highlights_json(json.dumps(db_copy))

def edit_clipping(entry = None):
    """Takes an entry and uses gui to ask for new entry."""
    if not entry:
        print('The ID provided below will be edited.')
        entry = search_by_id()




    menu = {
        1: "clipping",
        2: "author",
        3: "title",
        4: "timestamp"
    }

    for key in menu.keys():
        print(f'{key}: {menu[key]}')

    print('\n')
    


    selection_number = int(input("Select a field to edit using the number: "))

    key = menu[selection_number]
    entry[key] = get_new_text_from_user_gui(entry[key])

    return entry

def edit_entry_in_place():
    print('The ID provided below will be edited.')
    entry_to_edit = search_by_id()
    new_entry = edit_clipping(entry_to_edit)
    replace_entry(entry_to_edit, new_entry)

def entry_formatter(
    author: str = "No author",
    title: str = "No title",
    clipping: str = "No title",
    timestamp: str = "No timestamp",
    id: str = "No ID"
    ):

    ''' header = f"{title}, by {author}."

    
    return f"""
    {header}
    ----------------
    "{clipping}"

    Saved: {timestamp}
    """'''
    header = f"{title}, by {author}."

    
    return f"""
    {header}
    ----------------
    "{clipping}"

    Saved: {timestamp}
    ID: {id}
    """

def entry_formatter_for_full_entry(entry: dict):

    title = entry["title"]
    author = entry["author"]
    clipping = entry["clipping"]
    timestamp = entry["timestamp"]
    id = str(DATABASE["highlights"].index(entry))

    header = f"{title}, by {author}."

    
    return f"""
    {header}
    ----------------
    "{clipping}"

    Saved: {timestamp}
    ID: {id}
    """


def view_all():

    entries = [
        (entry, str(DATABASE["highlights"].index(entry)))
        for entry in DATABASE["highlights"]
    ]

    formatted_entries = ""

    for entry in entries:
        id = entry[1]
        entry = entry[0]
        entry_to_append = entry_formatter(
            author=entry["author"],
            title=entry["title"],
            clipping=entry["clipping"],
            timestamp=entry["timestamp"],
            id = id
            )

        formatted_entries = formatted_entries + entry_to_append + "\n"
    print(formatted_entries)

    return entries

def count_clippings():
    count = len(DATABASE["highlights"])
    print(count)
    return count

def interface():
    # menu = {
    #     1: delete_entries,
    #     2: search_by_clipping,
    #     3: search_by_id,
    #     4: edit_entry_in_place,
    #     5: count_clippings, 
    #     6: view_all
    # }

    funcs_and_user_friendly_names = [
        ("Delete entries", delete_entries),
        ("Search by: clipping contents", search_by_clipping),
        ("Search by: ID", search_by_id),
        ("Edit a clipping", edit_entry_in_place),
        ("Count clippings", count_clippings),
        ("View all clippings", view_all)
    ]
    
    print('\n')

    for count, menu_item in enumerate(funcs_and_user_friendly_names):
        print(f'{count + 1}: {menu_item[0]}')

    print('\n')
    selection = (int(input('Pick a value: '))) - 1
    funcs_and_user_friendly_names[selection][1]()
    #you can use the below to find required arguments for a function, and then ask for an input for each:
    #print(inspect.getfullargspec(search_by_clipping).args)
    


if __name__ == "__main__":
    interface()

    # pprint(
    #     delete_entries(
    #         DATABASE=utilities.read_bookmarks_highlights_json(),
    #         entries_to_delete=search_by_clipping()
    #         )
    # )
