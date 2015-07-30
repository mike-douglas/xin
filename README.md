# xin

A shell utility like `xargs` that sends each line of standard input to a command.

## Usage

`xin` works just like the incredibly useful `xargs` tool, except with one key difference: where `xargs` passes the standard input (STDIN) to the given command as command-line arguments, `xin` *passes each line of standard input to the given command*.

```
xin [-h] [-L num] [-B] [-P maxprocs] command [arguments...]

-h            Shows help
-L num        Send input into provided command in num-line chunks
-P maxprocs   Run in parallel mode with maxprocs jobs at a time
-B            In parallel, block after maxprocs tasks are started and wait
```

### Example

If you have a file that contains the following text, called `woods.txt`:

```
Whose woods these are I think I know.
His house is in the village though;
He will not see me stopping here
To watch his woods fill up with snow.
```

You can use `xin` to get a character count for *each line* by issuing the following command:

```bash
$ xin wc -c < woods.txt
      41
      39
      36
      38
```

`xin` takes each line from the file and invokes `wc -c`, passing the line in as standard input for that command.

`xin` pairs well with tools like [jq](http://stedolan.github.io/jq/) for processing large files containing `JSON` objects, and probably, like, dozens of other things. I pronounce it like 'zin', but 'jin' or 'x-in' works too.

## Prerequesites

Python >= 2.7

## Installation

```bash
$ pip install xin
```

or

```bash
$ git clone <this repo>
$ cd xin && python ./setup.py install
```
