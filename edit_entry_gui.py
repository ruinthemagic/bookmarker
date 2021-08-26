from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

def get_new_text_from_user_gui(text_to_edit = None):
    """Takes text input and asks the user to edit it"""
    global return_text
   
    return_text = text_to_edit
    
    root = Tk()

    if not text_to_edit:
        root.title("Enter text:")
    else:
        root.title("Edit text below:")

    # mainframe = ttk.Frame(root, padding="3 3 12 12")
    # mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    
    

    entry = scrolledtext.ScrolledText(root, width=40, height=10, wrap='word')
    entry.pack(expand=True, fill=BOTH)
    entry.insert('1.0', text_to_edit)

    def get_entry():
        global return_text
        return_text = entry.get('1.0', 'end')
        root.destroy()

        
    def remove_newlines():
        text_w_newlines = entry.get(1.0, 'end')
        entry.delete('1.0', 'end')
        entry.insert('1.0', text_w_newlines.replace('\n', ' '))
        

    button_remove_newlines = ttk.Button(root, text="Remove \\n", command=remove_newlines)
    button_remove_newlines.pack()

    button = ttk.Button(root, text="Submit", command=get_entry)
    button.pack()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()

    return return_text.strip()

if __name__ == "__main__":
    entry= "From my mother: piety, generosity, the avoidance of wrongdoing and even the thought of it; also simplicity of living, well clear of the habits of the rich."

    get_new_text_from_user_gui(entry)
