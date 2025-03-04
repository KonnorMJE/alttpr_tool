import os

def print_tree(directory, ignore_list=None, prefix="", is_last=True):
    """
    Print the tree structure of a directory.
    
    Args:
        directory (str): Path to the directory
        ignore_list (list): List of files/directories to ignore
        prefix (str): Prefix for the current line (used for recursion)
        is_last (bool): Whether this is the last item in current directory
    """
    if ignore_list is None:
        ignore_list = []
        
    # Get the base name of the directory
    base = os.path.basename(directory)
    
    # Print the current directory
    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}{base}")
    
    # Prepare the prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    # Get all items in directory
    items = [item for item in os.listdir(directory) 
            if item not in ignore_list and not item.startswith('.')]
    items.sort()
    
    # Print all subdirectories and files
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last_item = index == len(items) - 1
        
        if os.path.isdir(path):
            print_tree(path, ignore_list, child_prefix, is_last_item)
        else:
            child_connector = "└── " if is_last_item else "├── "
            print(f"{child_prefix}{child_connector}{item}")

# Example usage:
ignore = ['__pycache__', '.git', '.DS_Store', 'presets']
print_tree(".", ignore)