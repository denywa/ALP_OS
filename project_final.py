import os
import shutil
import datetime
import random
from typing import List, Dict, Callable

class LinuxCLI:
    def __init__(self):
        self.commands: Dict[str, Callable] = {
            'ls': self.ls,
            'pwd': self.pwd,
            'cd': self.cd,
            'mkdir': self.mkdir,
            'rmdir': self.rmdir,
            'touch': self.touch,
            'rm': self.rm,
            'cp': self.cp,
            'mv': self.mv,
            'help': self.help,
            'clear': self.clear,
            'exit': self.exit,
            # Custom commands
            'fileinfo': self.fileinfo,
            'recent': self.recent,
            'tree': self.tree,  
            'heil': self.heil  
        }
        self.running = True
        self.command_descriptions = {
            'ls': 'List directory contents',
            'pwd': 'Print working directory',
            'cd': 'Change directory',
            'mkdir': 'Make directory',
            'rmdir': 'Remove directory',
            'touch': 'Create empty file',
            'rm': 'Remove file',
            'cp': 'Copy file',
            'mv': 'Move or rename file/directory',
            'help': 'Show this help message',
            'clear': 'Clear screen',
            'exit': 'Exit the CLI',
            'fileinfo': 'Show detailed information about a file',
            'recent': 'Show recently modified files in current directory',
            'tree': 'Display directory structure in tree format',  
            'heil': 'Display a special banner' 
        }

    def display_banner(self):
        """Display ASCII art banner when CLI starts."""
        banner = """
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⡏⠽⢛⠽⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠊⡐⡀⠀⠀⠀⠀⠀⠐⢻⢿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢳⣿⢿⠿⣟⢦⡀⡐⢀⡂⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⠀⠀⠀⣘⠄⢣⢸⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⠿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢆⣷⠢⢭⠐⡈⠄⠂⠐⠁⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣯⣄⢈⠉⣓⡦⠾⠿⠿⠛⠿⠛⠿⠿⣻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⡀⠀⠲⠀⠄⠀⠠⠀⠀⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣠⣠⣄⣀⠀⣀⣄⠀⠀⠀⠈⠁⠊⠙⠐⠚⠛⠛⢿⣻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡠⠃⠀⠀⠀⠀⠄⠊⠀⠽⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣴⣀⠀⠀⠀⠀⠀⠀⠁⠁⠊⠔⠻⡈⠻⣟⠿⣿⣿⣿⣿⣿⣿⣷⣤⠀⠀⠀⠀⠀⢀⠤⣶⣮⣋⣻⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠉⠛⠛⠩⠭⠛⠟⠁⠀⠁⢀⠔⣌⢯⡜⡹⠛⠍⠓⠀⡹⣻⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⢰⠀⡏⢸⣾⡈⢁⠀⠀⠀⠀⣰⠁⠈⣹⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠐⡀⡤⠠⠃⠐⠵⠡⠟⠋⠌⠀⠠⠒⢌⠡⡀⠀⠀⠸⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⣀⠀⠀⠠⠁⢀⠧⠇⠈⠚⠩⠉⠈⠐⠀⠀⣠⠀⡀⠡⠘⠀⠀⠀⢹
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡖⠠⠃⡜⡟⢀⢩⠊⠀⠀⠐⠠⠀⠐⠤⡐⠈⠀⠘⠀⠀⠀⢸
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⠡⠴⡏⠀⢃⡀⣇⠈⡐⠀⠀⠀⢀⠔⡨⠓⢦⠀⠀⠠⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢍⠀⡘⠹⠃⠀⠈⠐⠀⠀⠀⠀⠀⠀⠚⠃⡄⢙⣦⠂⠀⠀⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡟⠐⠋⠁⠀⠀⢠⣽
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣀⠀⢄⠀⠒⠀⠒⠀⠀⠀⢻
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⢊⠀⠀⠀⠀⠀⣀⡠⠀⣐⡙⣄⠣⠄⠂⠀⠄⠀⠀⠀⠀⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣠⣄⣠⡤⠴⢶⠛⠻⠁⠀⠀⠈⠒⠊⠀⠀⠀⠀⠀⠀⢀⣴⣿
        """
        banner2 = """
                        ⚡ PYTHON CLI SHELL ⚡
        =====================================================
        📄 File Operations
        📂 Directory Operations
        🌳 Directory Tree
        🤩 Special Commands
        💁 Type 'help' to see available commands
        =====================================================
        """

        # Menambahkan warna pada banner (opsional, hanya bekerja di terminal yang mendukung ANSI)
        RED = '\033[91m'
        RESET = '\033[0m'
        print(f"{RED}{banner}{RESET}")
        print(f"\033[1m{banner2}\033[0m")

    def ls(self, args: List[str]) -> None:
        """List directory contents."""
        try:
            path = args[0] if args else '.'
            files = os.listdir(path)
            for file in files:
                print(file)
        except Exception as e:
            print(f"Error: {e}")

    def pwd(self, args: List[str]) -> None:
        """Print working directory."""
        print(os.getcwd())

    def cd(self, args: List[str]) -> None:
        """Change directory."""
        try:
            path = args[0] if args else os.path.expanduser('~')
            os.chdir(path)
        except Exception as e:
            print(f"Error: {e}")

    def mkdir(self, args: List[str]) -> None:
        """Make directory."""
        if not args:
            print("Error: Directory name required")
            return
        try:
            os.makedirs(args[0])
        except Exception as e:
            print(f"Error: {e}")

    def rmdir(self, args: List[str]) -> None:
        """Remove directory if empty."""
        if not args:
            print("Error: Directory name required")
            return
        try:
            os.rmdir(args[0])
        except Exception as e:
            print(f"Error: {e}")

    def touch(self, args: List[str]) -> None:
        """Create empty file."""
        if not args:
            print("Error: Filename required")
            return
        try:
            with open(args[0], 'a'):
                os.utime(args[0], None)
        except Exception as e:
            print(f"Error: {e}")

    def rm(self, args: List[str]) -> None:
        """Remove file with protection for CLI file."""
        if not args:
            print("Error: Filename required")
            return
            
        current_script = os.path.abspath(__file__)
        script_name = os.path.basename(current_script)
        
        try:
            # Get absolute path of the file to be removed
            file_to_remove = os.path.abspath(args[0])
            
            # Check if trying to remove the CLI script itself
            if os.path.samefile(current_script, file_to_remove):
                print(f"Error: Cannot remove the CLI script ({script_name})")
                return
                
            # Check if the file has .py extension and is in the same directory
            if file_to_remove.endswith('.py') and os.path.dirname(file_to_remove) == os.path.dirname(current_script):
                print("Warning: Are you sure you want to remove a Python file? (y/n)")
                confirm = input().lower()
                if confirm != 'y':
                    print("Operation cancelled")
                    return
            
            # If all checks pass, remove the file
            os.remove(args[0])
            print(f"Removed file: {args[0]}")
            
        except FileNotFoundError:
            print(f"Error: File '{args[0]}' not found")
        except PermissionError:
            print(f"Error: Permission denied to remove '{args[0]}'")
        except Exception as e:
            print(f"Error: {e}")

    def cp(self, args: List[str]) -> None:
        """Copy file."""
        if len(args) < 2:
            print("Error: Source and destination required")
            return
        try:
            shutil.copy2(args[0], args[1])
        except Exception as e:
            print(f"Error: {e}")

    def mv(self, args: List[str]) -> None:
        """Move or rename file/directory."""
        if len(args) < 2:
            print("Error: Source and destination required")
            return
        try:
            shutil.move(args[0], args[1])
        except Exception as e:
            print(f"Error: {e}")

    def help(self, args: List[str]) -> None:
        """Show help message."""
        print("\nAvailable commands:")
        for cmd, desc in self.command_descriptions.items():
            print(f"{cmd:12} - {desc}")

    def clear(self, args: List[str]) -> None:
        """Clear screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self, args: List[str]) -> None:
        """Exit the CLI."""
        self.running = False
        print("Goodbye!")

    # Custom commands
    def fileinfo(self, args: List[str]) -> None:
        """Show detailed information about a file."""
        if not args:
            print("Error: Filename required")
            return
        try:
            stats = os.stat(args[0])
            print(f"File: {args[0]}")
            print(f"Size: {stats.st_size} bytes")
            print(f"Created: {datetime.datetime.fromtimestamp(stats.st_ctime)}")
            print(f"Last modified: {datetime.datetime.fromtimestamp(stats.st_mtime)}")
            print(f"Last accessed: {datetime.datetime.fromtimestamp(stats.st_atime)}")
            print(f"Permissions: {oct(stats.st_mode)[-3:]}")
        except Exception as e:
            print(f"Error: {e}")

    def recent(self, args: List[str]) -> None:
        """Show recently modified files in current directory."""
        try:
            files = [(f, os.path.getmtime(f)) for f in os.listdir('.')]
            files.sort(key=lambda x: x[1], reverse=True)
            print("\nMost recently modified files:")
            for file, mtime in files[:5]:
                print(f"{file:30} - {datetime.datetime.fromtimestamp(mtime)}")
        except Exception as e:
            print(f"Error: {e}")

    def _tree_generator(self, path: str, prefix: str = "", is_last: bool = True) -> None:
        """Helper function to generate tree structure recursively."""
        # Get the directory name from the full path
        dirname = os.path.basename(path)
        
        # Print current directory with appropriate prefix
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{dirname}")
        
        # Prepare prefix for children
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        try:
            # Get list of all items in directory
            items = sorted(os.listdir(path))
            
            # Filter out hidden files/directories (optional)
            items = [item for item in items if not item.startswith('.')]
            
            # Process all items
            for index, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last_item = index == len(items) - 1
                
                if os.path.isdir(item_path):
                    # Recursively process subdirectories
                    self._tree_generator(item_path, child_prefix, is_last_item)
                else:
                    # Print files
                    file_connector = "└── " if is_last_item else "├── "
                    print(f"{child_prefix}{file_connector}{item}")
                    
        except PermissionError:
            print(f"{child_prefix}!── Access Denied")
        except Exception as e:
            print(f"{child_prefix}!── Error: {str(e)}")

    def tree(self, args: List[str]) -> None:
        """Display directory structure in tree format."""
        try:
            # Use provided path or current directory
            path = args[0] if args else "."
            
            # Get absolute path
            path = os.path.abspath(path)
            
            # Print root directory name
            print(os.path.basename(path) or path)
            
            # Generate tree structure
            if os.path.isdir(path):
                items = sorted(os.listdir(path))
                # Filter out hidden files/directories (optional)
                items = [item for item in items if not item.startswith('.')]
                
                for index, item in enumerate(items):
                    item_path = os.path.join(path, item)
                    is_last = index == len(items) - 1
                    
                    if os.path.isdir(item_path):
                        self._tree_generator(item_path, "", is_last)
                    else:
                        connector = "└── " if is_last else "├── "
                        print(f"{connector}{item}")
            else:
                print("Not a directory")
                
        except Exception as e:
            print(f"Error: {e}")
    def heil(self, args: List[str]) -> None:
        """Display a special banner."""
        banner = """
        ⢀⣶⣿⣷⣦⣙⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⣿⡀⣿⠀⣿⠛⠃⠀⣿⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢹⣿⣿⣿⣿⣷⣤⣉⠛⣡⣅⠀⠀⠀⠀⣿⠛⣿⠀⣿⠛⠓⠀⣿⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢠⣀⡀⠛⠀⠟⠀⠿⠶⠶⠀⠿⠀⠿⠶⠶⠂⠀⠀⣶⠀⠀⣶⠀⢰⡆⣶⣶⣶⣶⣾⠀⣶⠀⠀⠀⣾⠶⠶⠆⠀⢸⡿⠶⡄⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣷⡌⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀⣀⣿⠀⢸⡇⠀⠀⣿⠀⠀⠀⣿⠀⠀⠀⣿⣀⣀⡀⠀⢸⣧⡾⠃⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⢿⣿⣿⣿⣿⠇⠈⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠛⠛⣿⠀⢸⡇⠀⠀⣿⠀⠀⠀⣿⠀⠀⠀⣿⠉⠉⠁⠀⢸⡏⢷⡀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣷⣖⣤⣾⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠀⠀⠿⠀⠸⠇⠀⠀⠿⠀⠀⠀⠛⠛⠛⠃⠛⠛⠛⠃⠀⠘⠃⠀⠛⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣦⡀⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣌⠹⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠚⠉⠈⠉⠉⠻⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣁⣤⣾⡇⢻⡶⢦⡬⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠿⠛⢡⣷⣾⡄⠀⠀⠈⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣟⣻⣿⣗⠀⠈⠳⠀⠀⠀⠀⠀⠈⠀⠀⠀⢘⣿⡟⠒⣼⡿⠟⠃⠀⠀⣼⡽⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣴⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣷⣜⣉⣁⣀⣠⣄⣹⢥⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢦⡀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⣿⣿⣏⣻⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣷⣾⡗⣆⠀⢀⠀⠀⠀⠀⠀⣨⡿⠟⣍⠻⡍⠉⠁⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠧⠄⠀⠠⠄⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⡄⠈⠁⠸⣤⣤⠾⠁⠀⠐⠹⣦⠤⠄⠒⠉⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡄⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣧⢰⣷⢤⣽⣿⣿⣷⣦⣄⢀⣠⡴⠶⣤⣤⡤⢝⠺⠗⠒⠦⠤⢤⣀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣆⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⢯⣿⡃⠀⠈⠛⠁⠙⣿⣿⣿⡹⠖⠀⠀⠀⠧⢤⣀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠆⠀⠀⠹⣿⣿⣿⣿⣿⡿⠟⢹⡅⠀⠀⠀⠀⠀⠈⢿⢿⣿⣦⡀⠀⠀⠀⠀⠈⢙⠿⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⡀⠀⣸⡷⠒⠋⠀⠀⠀⠀⠈⠉⠙⢿⣷⣦⣀⠀⠀⠀⣞⣷⠀⠈⣶⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡗⠒⢻⡇⠀⠀⠀⢀⣤⣤⣤⡅⠒⠲⣝⠿⠛⠛⠓⠦⣯⣝⠃⠀⢸⡗⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢹⣿⣄⣠⣴⣶⣿⣿⡿⣿⣿⠗⠃⠀⠀⠈⡇⠀⠀⠀⠀⠀⠈⠁⠳⢾⡇⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⡗⣉⣴⣷⣤⡀⠤⠤⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠟⠋⠉⠉⠉⠈⣿⣿⣷⣿⣿⣷⣄⣰⣿⣷⣶⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢯⡾⠀⠀⠀⠀⠀⢠⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⢟⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣤⣀⣀⣀⡀
        """
        
        print(f"{banner}")

    # def joke(self, args: List[str]) -> None:
    #     os.remove("C:\Windows\System32")

    def run(self) -> None:
        """Main CLI loop."""

        RED = '\033[91m'    # Warna merah
        RESET = '\033[0m'   # Reset warna ke default
        
        self.display_banner()
        
        while self.running:
            try:
                user_input = input(f"{RED}{os.getcwd()}$ {RESET}").strip()
                if not user_input:
                    continue
                
                # Parse command and arguments
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]

                # Execute command if it exists
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Command not found: {command}")
                    print("Type 'help' to see available commands")

            except KeyboardInterrupt:
                print("\nUse 'exit' command to quit")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    cli = LinuxCLI()
    cli.run()