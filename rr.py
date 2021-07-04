import os
import sys
import shutil
import tarfile
import pathlib
import re
import tempfile

# Path where our script is stored
self_path = os.path.dirname(os.path.abspath(__file__))

# Path where we should write extracted files to
out_dir = tempfile.mkdtemp()


# Log to the console in pretty colors
def log(text):
    print(f'\033[94m{text}\033[0m')


# Display usage to the user
def usage():
    log('s: select regex pattern')
    log('n: narrow search further')
    log('x: extract selected items')
    log('r: erase output directory')
    log('q: quit')
    log('h: show basic usage')


# Class for handling user selections
class Selector:
    # Map of tar file paths to tar file content paths
    # i.e.: { '/path/to/test.tar': ['1.txt', '2.txt', etc.] }
    selected_tar_map = {}

    def __init__(self):
        self.initial_tar_map = enumerate_tars()

    # Process user-input from the command line
    def ui(self):
        # Request input
        raw_cmd = input('rr> ')
        raw_cmd_split = raw_cmd.split()

        # Handle edge case where no input
        if len(raw_cmd_split) == 0:
            return

        # Split into command and arguments
        cmd = raw_cmd_split[0]
        args = ' '.join(raw_cmd_split[1:])

        # Select recursively via regex pattern
        if cmd == 's':
            self.selected_tar_map = search(self.initial_tar_map, args)

            # Tell the user what we found
            cnt = sum([len(self.selected_tar_map[x]) for x in self.selected_tar_map.keys()])
            log(f'found: {cnt}')
        elif cmd == 'n':
            self.selected_tar_map = search(self.selected_tar_map, args)

            # Tell the user what we found
            cnt = sum([len(self.selected_tar_map[x]) for x in self.selected_tar_map.keys()])
            log(f'narrowed to: {cnt}')
        # List selected items
        elif cmd == 'l':
            for tar_path in self.selected_tar_map.keys():
                log(f'tar: {tar_path}')
                for tar_name in self.selected_tar_map[tar_path]:
                    log(f'\t| file: {tar_name}')
        # Extracts selected items
        elif cmd == 'x':
            # Create output directory if nonexistent
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            # For each file, extract it
            for tar_path in self.selected_tar_map.keys():
                tar_file = tarfile.open(tar_path)
                for tar_name in self.selected_tar_map[tar_path]:
                    log(f'x [{out_dir}]: {tar_name}')
                    tar_file.extract(tar_name, out_dir)
                tar_file.close()
        # Erase output directory
        elif cmd == 'r':
            shutil.rmtree(out_dir, ignore_errors=True)
            log('erased output directory')
        # Show usage
        elif cmd == 'h':
            usage()
        # Quit
        elif cmd == 'q':
            sys.exit()
        # Not sure
        else:
            log(f'unknown action: {cmd}')


# Return a map of all tarballs to their contents
def enumerate_tars():
    tar_map = {}
    for root, _, files in os.walk(self_path):
        for filename in files:
            tar_path = os.path.join(root, filename)
            suffixes = pathlib.Path(filename).suffixes
            # Only find files with a tar suffix
            if '.tar' in suffixes:
                tar = tarfile.open(tar_path)
                tar_names = tar.getnames()
                tar.close()
                tar_map[tar_path] = tar_names
    return tar_map


# Narrow an existing search for a regex
def search(tar_map, pattern):
    new_tar_map = {}
    for tar_path in tar_map.keys():
        tar_members = []
        for tar_name in tar_map[tar_path]:
            if re.match(pattern, tar_name) is not None:
                tar_members.append(tar_name)
        new_tar_map[tar_path] = tar_members
    return new_tar_map


# Main selector loop
def main():
    selector = Selector()
    while True:
        selector.ui()


if __name__ == '__main__':
    main()
