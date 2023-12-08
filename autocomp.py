import os
from tkinter import Frame, Tk, Listbox, Scrollbar, Entry, END, BOTH, StringVar
import pyperclip
import csv
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController


def load_data(file_path):
    with open(file_path, newline="") as lines:
        lines_reader = csv.reader(lines, delimiter="\t")
        lines_reader = sorted(lines_reader, key=lambda row: int(row[1]), reverse=True)
        return list(lines_reader)


def update_data(lines_reader, selected_text, file_path):
    for row in lines_reader:
        if row[0] == selected_text:
            row[1] = str(int(row[1]) + 1)

    with open(file_path, "w", newline="") as lines_out:
        writer = csv.writer(
            lines_out, delimiter="\t", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        writer.writerows(lines_reader)


def on_entry_enter(event):
    selected_text = listbox.get(listbox.curselection())
    root.destroy()

    pyperclip.copy(selected_text)

    keyboard.press(Key.ctrl)
    keyboard.press("v")
    keyboard.release("v")
    keyboard.release(Key.ctrl)

    update_data(lines_reader, selected_text, file_path)


def on_escape(event):
    update_data(lines_reader, entry_var.get(), file_path)
    root.destroy()


def on_up(event):
    listbox.select_set(1)
    listbox.event_generate("<<ListboxSelect>>")


def on_down(event):
    print("Test")


def on_add_entry(event):
    new_entry = entry_var.get()

    # Check if entry already exists in lines_reader
    entry_exists = False
    for entry_data in lines_reader:
        if entry_data[0] == new_entry:
            entry_data[1] = str(int(entry_data[1]) + 1)
            entry_exists = True
            break

    if not entry_exists:
        # Entry is not in lines_reader, add it with count 1
        lines_reader.append([new_entry, str(1)])

    listbox.insert(END, new_entry)
    entry_var.set("")

    update_data(lines_reader, entry_var.get(), file_path)
    root.destroy()


def main():
    # File path
    global file_path
    file_path = os.path.expanduser("~/.autocomp/list.txt")

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file if it doesn't exist
        with open(file_path, "w") as file:
            pass

    # Mouse and keyboard controllers
    global mouse
    mouse = MouseController()
    global keyboard
    keyboard = KeyboardController()

    # Tkinter setup
    global root
    root = Tk()
    root.geometry("+%d+%d" % (mouse.position[0], mouse.position[1]))
    root.attributes("-topmost", True)
    root.wm_attributes("-type", "splash")
    root.update()
    root.focus_force()

    # Frame to group Listbox and Scrollbar
    list_frame = Frame(root)
    list_frame.pack(side="top", fill=BOTH, expand=True)

    global listbox
    listbox = Listbox(list_frame)
    listbox.pack(side="left", fill=BOTH, expand=True)

    scrollbar = Scrollbar(list_frame, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)

    # Input box setup
    global entry_var
    entry_var = StringVar()
    entry = Entry(root, textvariable=entry_var)
    entry.pack(side="bottom", fill=BOTH)

    # Load data and populate listbox
    global lines_reader
    lines_reader = load_data(file_path)
    for line in lines_reader:
        listbox.insert(END, line[0])

    # Event bindings
    listbox.bind("<Return>", on_entry_enter)
    listbox.bind("<Escape>", on_escape)
    listbox.bind("<Up>", on_up)
    listbox.bind("<Down>", on_down)
    listbox.bind("<Tab>", lambda event: entry.focus_set())
    entry.bind("<Return>", on_add_entry)
    entry.bind("<Escape>", on_escape)

    listbox.select_set(0)
    listbox.event_generate("<<ListboxSelect>>")

    listbox.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
