import os
import sys
import argparse

def print_tree(directory, ignore_list=None, summarize_list=None, prefix="", is_last=True):
    """
    Print the tree structure of a directory.
    
    Args:
        directory (str): Path to the directory
        ignore_list (list): List of files/directories to ignore
        summarize_list (list): List of [directory_name, description] pairs to summarize
        prefix (str): Prefix for the current line (used for recursion)
        is_last (bool): Whether this is the last item in current directory
    """
    if ignore_list is None:
        ignore_list = ['__pycache__', '.git', '.DS_Store', 'venv', 'old_alttpr_tool']
    if summarize_list is None:
        summarize_list = []
        
    # Convert summarize_list to dict for easier lookup
    summarize_dict = dict(summarize_list)
        
    # Get the base name of the directory
    base = os.path.basename(directory)
    
    # Print the current directory
    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}{base}")
    
    # If this directory is in summarize_list, print its description and return
    if base in summarize_dict:
        
        child_prefix = prefix + ("    " if is_last else "│   ")
        child_connector = "└── "
        print(f"{child_prefix}{child_connector}[{summarize_dict[base]}]")
        return
    
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
            print_tree(path, ignore_list, summarize_list, child_prefix, is_last_item)
        else:
            child_connector = "└── " if is_last_item else "├── "
            print(f"{child_prefix}{child_connector}{item}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print a directory tree structure')
    parser.add_argument('path', nargs='?', default='.', 
                       help='Path to the directory (defaults to current directory)')
    parser.add_argument('--ignore', nargs='+', default=['__pycache__', '.git', '.DS_Store', 'presets', 'venv'],
                       help='List of directories/files to ignore')
    parser.add_argument('--summarize', nargs='+', default=[],
                       help='List of directory:description pairs to summarize (e.g., "presets:Contains preset files")')
    
    args = parser.parse_args()
    
    # Convert relative path to absolute path
    directory = os.path.abspath(args.path)
    
    # Convert summarize arguments to list of pairs
    summarize_pairs = []
    for pair in args.summarize:
        if ':' in pair:
            dir_name, description = pair.split(':', 1)
            summarize_pairs.append([dir_name, description])
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory")
        sys.exit(1)
        
    print(f"\nDirectory tree for: {directory}\n")
    print_tree(directory, args.ignore, summarize_pairs)