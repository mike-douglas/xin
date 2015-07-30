from __future__ import print_function

import sys
import os
import subprocess

from multiprocessing import Pool

class InvalidArgumentException(Exception):
    def __init__(self, attribute, message):
        self.attribute = attribute
        self.message = message

def get_help(error=None):
    if not error is None:
        error = 'error: {}\n'.format(error)
    return """{error}{this} - xargs but for standard input

Usage:
    {this} [-h] [-L num] [-B] [-P maxprocs] command [arguments...]

    -h            Shows help
    -L num        Send input into provided command in num-line chunks
    -P maxprocs   Run in parallel mode with maxprocs jobs at a time
    -B            In parallel, block after maxprocs tasks are started and wait
""".format(error=error, this=os.path.split(sys.argv[0])[-1]).strip()

def run_utility(arguments, line):
    p = subprocess.Popen(arguments, stdin=subprocess.PIPE,\
                                    stdout=subprocess.PIPE,\
                                    stderr=subprocess.PIPE)
    output, error = p.communicate(line)

    if p.returncode is None:
        p.terminate()

    return output, error

def output_result(output, error, stdout=None):
    if stdout == None:
        stdout = sys.stdout
    if not output is None:
        print(output, end='', file=stdout)
    if not error is None:
        print(error, end='', file=stdout)

def chunked_lines(handle, chunk_size=1):
    chunks = []

    for line in handle.readlines():
        chunks.append(line)
        if len(chunks) == chunk_size:
            yield ''.join(chunks)
            chunks = []

    if len(chunks) > 0 and len(chunks) < chunk_size:
        yield ''.join(chunks)

def parse_arguments(arguments):
    flags = {
        '-L': 1,
        '-P': None,
        '-B': False,
    }
    command = []
    skipped_arguments = []

    for n in xrange(len(arguments)):
        if n in skipped_arguments:
            continue

        arg = arguments[n]
        if arg[0:2] in ('-L', '-P'): # Integer-based arguments
            try:
                if len(arg) > 2:
                    flags[arg[0:2]] = int(arg[2:])
                else:
                    flags[arg] = int(arguments[n+1])
                    skipped_arguments.append(n+1)
            except ValueError, e:
                raise InvalidArgumentException(arg, 'Invalid value')
        elif arg[0:2] in ('-B'):
            flags[arg] = True
        elif arg in ('-h', '--h', '--help'): # Halp
            raise Exception('Showing help')
        else: # Everything else should be a command
            command.append(arg)

    if len(command) == 0:
        raise Exception('Missing command')
    elif command[0].startswith('-'):
        raise Exception('Command is invalid')

    return flags, command

def main():
    try:
        flags, command = parse_arguments(sys.argv[1:])
    except InvalidArgumentException, e:
        print(get_help('{msg} for {attr}'.format(attr=e.attribute, msg=e.message)))
        sys.exit(1)
    except Exception, e:
        print(get_help(e))
        sys.exit(1)

    try:
        with sys.stdin as file_handle:
            chunked_iterator = chunked_lines(file_handle, flags['-L'])

            if flags['-P'] is None or flags['-P'] == 1:
                for line in chunked_iterator:
                    output_result(*run_utility(command, line))
            else:
                pool = Pool(flags['-P'])
                results = []

                def empty_pool(r):
                    for item in r:
                        output_result(*item.get())

                for line in chunked_iterator:
                    results.append(pool.apply_async(run_utility, args=(command, line)))
                    if flags['-B'] is True and len(results) == flags['-P']:
                        pool.close()
                        pool.join()

                        empty_pool(results)

                        results = []
                        pool = Pool(flags['-P'])

                pool.close()
                pool.join()

                empty_pool(results)
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    main()