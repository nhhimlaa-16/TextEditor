import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, colorchooser

# Create the main window
root = tk.Tk()
root.title("Notepad 11.2508.38.0")
root.geometry("800x600")

# Global variables to track current text widget and file
current_text = None
current_file = None
status_visible = True

# Create notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Function to add a new tab
def add_tab(file_path=None, content=""):
    global current_text, current_file
    tab_frame = tk.Frame(notebook)
    text_widget = tk.Text(tab_frame, wrap="word", undo=True)
    text_widget.pack(expand=True, fill="both")
    text_widget.insert(tk.END, content)
    tab_name = "Untitled" if not file_path else file_path.split("/")[-1]
    notebook.add(tab_frame, text=tab_name)
    if not current_text:  # Set as current if it's the first tab
        current_text = text_widget
        current_file = file_path
    return text_widget, file_path

# Initial tab
current_text, current_file = add_tab()

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

def new_file():
    global current_text, current_file
    if current_text.get("1.0", tk.END).strip():
        if messagebox.askyesno("Unsaved Changes", "Do you want to save changes?"):
            save_file()
    current_text, current_file = add_tab()
    root.title("Notepad 11.2508.38.0")

def open_file():
    global current_text, current_file
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            current_text, current_file = add_tab(file_path, file.read())
        root.title(f"Notepad 11.2508.38.0 - {file_path}")

def save_file():
    global current_file
    if current_file:
        with open(current_file, "w") as file:
            file.write(current_text.get("1.0", tk.END))
    else:
        save_as_file()

def save_as_file():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(current_text.get("1.0", tk.END))
        current_file = file_path
        root.title(f"Notepad 11.2508.38.0 - {file_path}")

def open_in_new_tab():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            add_tab(file_path, file.read())
            root.title(f"Notepad 11.2508.38.0 - {file_path}")

# Add menu items
file_menu.add_command(label="New File", command=new_file)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save / Save As", command=save_file)
file_menu.add_command(label="Open in New Tab", command=open_in_new_tab)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

def get_current_text_widget():
    current_tab = notebook.select()
    if current_tab:
        return notebook.nametowidget(current_tab).winfo_children()[0]
    return current_text

def undo():
    current_text = get_current_text_widget()
    if current_text:
        current_text.event_generate("<<Undo>>")

def redo():
    current_text = get_current_text_widget()
    if current_text:
        current_text.event_generate("<<Redo>>")

def cut():
    current_text = get_current_text_widget()
    if current_text:
        current_text.event_generate("<<Cut>>")

def copy():
    current_text = get_current_text_widget()
    if current_text:
        current_text.event_generate("<<Copy>>")

def paste():
    current_text = get_current_text_widget()
    if current_text:
        current_text.event_generate("<<Paste>>")

def select_all():
    current_text = get_current_text_widget()
    if current_text:
        current_text.tag_add("sel", "1.0", "end")

def clear_text():
    current_text = get_current_text_widget()
    if current_text:
        current_text.delete("1.0", tk.END)

def find_and_navigate():
    search_text = simpledialog.askstring("Find", "Enter text to find:")
    if search_text:
        current_text = get_current_text_widget()
        if current_text:
            current_text.tag_remove("highlight", "1.0", tk.END)
            start = "1.0"
            positions = []
            while True:
                start = current_text.search(search_text, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(search_text)}c"
                positions.append((start, end))
                start = end
            if positions:
                current_text.tag_config("highlight", background="yellow")
                for start, end in positions:
                    current_text.tag_add("highlight", start, end)
                # Simple Find Next (cycle through positions)
                current_pos = 0
                def find_next():
                    nonlocal current_pos
                    if positions:
                        current_pos = (current_pos + 1) % len(positions)
                        start, end = positions[current_pos]
                        current_text.tag_remove("sel", "1.0", tk.END)
                        current_text.tag_add("sel", start, end)
                        current_text.see(start)
                root.bind("<Control-g>", lambda e: find_next())  # Ctrl+G for Find Next

# Add menu items
edit_menu.add_command(label="Undo / Redo", command=lambda: [undo(), redo()])
edit_menu.add_command(label="Cut / Copy / Paste", command=lambda: [cut(), copy(), paste()])
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_command(label="Clear Text", command=clear_text)
edit_menu.add_command(label="Find & Highlight / Find Next / Find All", command=find_and_navigate)

# Search & Replace menu
search_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Search & Replace", menu=search_menu)

def replace_text():
    search_text = simpledialog.askstring("Replace", "Enter text to find:")
    if search_text:
        replace_text = simpledialog.askstring("Replace", "Enter replacement:")
        current_text = get_current_text_widget()
        if current_text:
            content = current_text.get("1.0", tk.END)
            new_content = content.replace(search_text, replace_text)
            current_text.delete("1.0", tk.END)
            current_text.insert(tk.END, new_content)

# Add menu items
search_menu.add_command(label="Keyword search", command=find_and_navigate)
search_menu.add_command(label="Replace text", command=replace_text)
search_menu.add_command(label="Highlight all matches", command=find_and_navigate)

# Auto Completion menu
auto_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Auto Completion", menu=auto_menu)

# Define keywords for auto completion
java_keywords = ["public", "class", "static", "void"]
cpp_keywords = ["int", "float", "if", "else"]
python_keywords = ["if", "else", "elif", "for", "while", "def", "class", "return", "print", "import"]
basic_suggestions = ["hello", "world", "test"]

def auto_complete(keywords):
    current_text = get_current_text_widget()
    if current_text:
        current = current_text.get("insert-1c", "insert")
        for word in keywords:
            if word.startswith(current):
                current_text.delete("insert-1c", "insert")
                current_text.insert("insert", word)
                break

# Add menu items
auto_menu.add_command(label="Java keywords", command=lambda: auto_complete(java_keywords))
auto_menu.add_command(label="C++ keywords", command=lambda: auto_complete(cpp_keywords))
auto_menu.add_command(label="Python keywords", command=lambda: auto_complete(python_keywords))
auto_menu.add_command(label="Basic autocomplete suggestions", command=lambda: auto_complete(basic_suggestions))

import tkinter.font as tkfont

# Text Formatting menu
format_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Text Formatting", menu=format_menu)

def change_font_family():
    current_text = get_current_text_widget()
    if current_text:
        fonts = list(tkfont.families())
        chosen_font = simpledialog.askstring("Font Family", "Enter font family (e.g., Arial):")
        if chosen_font in fonts:
            current_text.config(font=(chosen_font, current_text.cget("font")[1]))

def change_font_size():
    current_text = get_current_text_widget()
    if current_text:
        size = simpledialog.askinteger("Font Size", "Enter size (e.g., 12):", minvalue=1, maxvalue=100)
        if size:
            current_font = current_text.cget("font")[0]
            current_text.config(font=(current_font, size))

def toggle_bold():
    current_text = get_current_text_widget()
    if current_text:
        current_font = tkfont.Font(font=current_text["font"])
        current_text.config(font=(current_font.actual()["family"], current_font.actual()["size"], "bold" if "bold" not in current_font.actual() else ""))

def toggle_italic():
    current_text = get_current_text_widget()
    if current_text:
        current_font = tkfont.Font(font=current_text["font"])
        current_text.config(font=(current_font.actual()["family"], current_font.actual()["size"], "italic" if "italic" not in current_font.actual() else ""))

def change_text_color():
    current_text = get_current_text_widget()
    if current_text:
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            current_text.config(foreground=color)

def change_background_color():
    current_text = get_current_text_widget()
    if current_text:
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            current_text.config(background=color)

# Add menu items
format_menu.add_command(label="Font family change", command=change_font_family)
format_menu.add_command(label="Font size change", command=change_font_size)
format_menu.add_command(label="Bold / Italic (optional)", command=lambda: [toggle_bold(), toggle_italic()])
format_menu.add_command(label="Text color", command=change_text_color)
format_menu.add_command(label="Background color", command=change_background_color)


# View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)

zoom_level = 100

def zoom_in():
    global zoom_level
    zoom_level += 10
    update_zoom()

def zoom_out():
    global zoom_level
    if zoom_level > 10:
        zoom_level -= 10
    update_zoom()

def reset_zoom():
    global zoom_level
    zoom_level = 100
    update_zoom()

def update_zoom():
    current_text = get_current_text_widget()
    if current_text:
        current_font = current_text.cget("font")
        new_size = int(12 * (zoom_level / 100))
        current_text.config(font=(current_font[0], new_size))

def toggle_word_wrap():
    current_text = get_current_text_widget()
    if current_text:
        if current_text.cget("wrap") == "word":
            current_text.config(wrap="none")
        else:
            current_text.config(wrap="word")

def toggle_status_bar():
    global status_visible
    if status_visible:
        status_bar.pack_forget()
    else:
        status_bar.pack(side="bottom", fill="x")
    status_visible = not status_visible

# Add menu items
view_menu.add_command(label="Zoom In", command=zoom_in)
view_menu.add_command(label="Zoom Out", command=zoom_out)
view_menu.add_command(label="Reset Zoom", command=reset_zoom)
view_menu.add_command(label="Word wrap toggle", command=toggle_word_wrap)
view_menu.add_command(label="Show/Hide status bar", command=toggle_status_bar)

# Tools menu
tools_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tools", menu=tools_menu)

def word_count():
    current_text = get_current_text_widget()
    if current_text:
        content = current_text.get("1.0", tk.END).strip()
        words = len([word for word in content.split() if word])  # Filter out empty strings
        messagebox.showinfo("Word Count", f"Words: {words}")

def character_count():
    current_text = get_current_text_widget()
    if current_text:
        content = current_text.get("1.0", tk.END)
        chars = len(content.rstrip())  # Remove trailing newline(s) accurately
        messagebox.showinfo("Character Count", f"Characters: {chars}")

def line_count():
    current_text = get_current_text_widget()
    if current_text:
        content = current_text.get("1.0", tk.END)
        lines = content.count('\n') + 1 if content.strip() else 1
        messagebox.showinfo("Line Count", f"Lines: {lines}")

def cursor_position():
    current_text = get_current_text_widget()
    if current_text:
        try:
            pos = current_text.index(tk.INSERT)
            line, col = map(int, pos.split('.'))
            messagebox.showinfo("Cursor Position", f"Line: {line}, Column: {col}")
        except (ValueError, tk.TclError):
            messagebox.showinfo("Cursor Position", "Line: 1, Column: 0")

# Add menu items
tools_menu.add_command(label="Word count", command=word_count)
tools_menu.add_command(label="Character count", command=character_count)
tools_menu.add_command(label="Line count", command=line_count)
tools_menu.add_command(label="Cursor position (Ln, Col)", command=cursor_position)

def drop(event):
    file_path = event.data
    if file_path:
        with open(file_path, "r") as file:
            add_tab(file_path, file.read())
            root.title(f"Notepad 11.2508.38.0 - {file_path}")

def drop(event):
    file_path = event.data
    if file_path:
        with open(file_path, "r") as file:
            add_tab(file_path, file.read())
            root.title(f"Notepad 11.2508.38.0 - {file_path}")


# Toolbar
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

tk.Button(toolbar, text="New", command=new_file).pack(side="left")
tk.Button(toolbar, text="Open", command=open_file).pack(side="left")
tk.Button(toolbar, text="Save", command=save_file).pack(side="left")
tk.Button(toolbar, text="Cut", command=cut).pack(side="left")
tk.Button(toolbar, text="Copy", command=copy).pack(side="left")
tk.Button(toolbar, text="Paste", command=paste).pack(side="left")
tk.Button(toolbar, text="Undo", command=undo).pack(side="left")
tk.Button(toolbar, text="Redo", command=redo).pack(side="left")
tk.Button(toolbar, text="Zoom", command=zoom_in).pack(side="left")
tk.Button(toolbar, text="Search", command=find_and_navigate).pack(side="left")
# About menu
about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)

def show_about():
    message = "Notepad 11.2508.38.0\nDeveloped by: Your Name\nLicense: MIT"
    messagebox.showinfo("About", message)

about_menu.add_command(label="Version info", command=show_about)
about_menu.add_command(label="Developer info", command=show_about)
about_menu.add_command(label="License", command=show_about)

# Keyboard shortcuts
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-Shift-S>", lambda e: save_as_file())
root.bind("<Control-f>", lambda e: find())
root.bind("<Control-h>", lambda e: replace_text())
root.bind("<Control-plus>", lambda e: zoom_in())
root.bind("<Control-minus>", lambda e: zoom_out())
root.bind("<Control-0>", lambda e: reset_zoom())
root.bind("<Control-z>", lambda e: undo())
root.bind("<Control-y>", lambda e: redo())
root.bind("<Control-a>", lambda e: select_all())

# Statusbar
status_bar = tk.Label(root, text="Ready", anchor="w", relief="sunken")
status_bar.pack(side="bottom", fill="x")

def update_status(event=None):
    current_text = get_current_text_widget()
    if current_text:
        pos = current_text.index(tk.INSERT)
        line, col = pos.split('.')
        status_bar.config(text=f"Ln {line}, Col {col} | Ready")

root.bind("<KeyRelease>", update_status)


# Run the application
root.mainloop()