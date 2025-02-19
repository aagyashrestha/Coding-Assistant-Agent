from langchain_core.tools import tool  # Import the 'tool' decorator from LangChain

@tool  # Mark this function as a tool for LangChain
def note_tool(note):  # Define a function that takes a note as input
    """
    Saves a note to a local file.

    Args:
        note: The text note to save.
    """
    with open("notes.txt", "a") as f:  # Open (or create) a file called "notes.txt" in append mode
        f.write(note + "\n")  # Write the note to the file and move to a new line
