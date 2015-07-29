from __future__ import print_function

import os
import sys
import subprocess

def get_help():
    return """
{this}
usage: {this} [utility [argument ...]]
""".format(this=os.path.split(sys.argv[0])[-1]).strip()

def run_utility(arguments, line):
    p = subprocess.Popen(arguments, stdin=subprocess.PIPE)
    p.communicate(line)

    if p.returncode is None:
        p.terminate()

def main():
    if len(sys.argv) == 1:
        print(get_help(), file=sys.stderr)
        sys.exit(1)

    command_arguments = sys.argv[1:]

    try:
        with sys.stdin as file_handle:
            for line in file_handle.readlines():
                run_utility(command_arguments, line)

    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    main()