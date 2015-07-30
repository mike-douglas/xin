import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

woods_txt = """Whose woods these are I think I know.
His house is in the village though;
He will not see me stopping here
To watch his woods fill up with snow.
My little horse must think it queer
To stop without a farmhouse near
Between the woods and frozen lake
The darkest evening of the year.
He gives his harness bells a shake
To ask if there is some mistake.
The only other sound's the sweep
Of easy wind and downy flake.
The woods are lovely, dark and deep,
But I have promises to keep,
And miles to go before I sleep,
And miles to go before I sleep.
"""

class TestOutputResult(unittest.TestCase):
    def setUp(self):
        self.stdout_expected = 'This is standard out.'
        self.stderr_expected = 'This is standard error.'
        self.output = StringIO()
        self.stdboth = ''.join([self.stdout_expected, self.stderr_expected])

    def test_output_only_stdout(self):
        from xin import output_result

        output_result(self.stdout_expected, None, stdout=self.output)

        self.assertEquals(self.output.getvalue(), self.stdout_expected)

    def test_output_only_stderr(self):
        from xin import output_result

        output_result(None, self.stderr_expected, stdout=self.output)

        self.assertEquals(self.output.getvalue(), self.stderr_expected)

    def test_output_neither(self):
        from xin import output_result

        output_result(None, None, stdout=self.output)

        self.assertEquals(self.output.getvalue(), '')

    def test_output_both(self):
        from xin import output_result

        output_result(self.stdout_expected, self.stderr_expected, stdout=self.output)

        self.assertEquals(self.output.getvalue(), self.stdboth)

class TestLineChunking(unittest.TestCase):
    def setUp(self):
        self.woods_file = StringIO(woods_txt)

    def test_chunk_lines_default(self):
        from xin import chunked_lines

        num_lines = len(woods_txt.split('\n')) - 1
        self.assertEquals(num_lines, len(list(chunked_lines(self.woods_file))))

    def test_chunk_lines_size_n(self):
        from xin import chunked_lines

        def woods_excerpt(start, end):
            return '\n'.join(woods_txt.split('\n')[start:end]) + '\n'

        def new_woods_file():
            return StringIO(woods_txt)

        self.assertEquals(woods_excerpt(0, 5), list(chunked_lines(new_woods_file(), 5))[0])
        self.assertEquals(woods_excerpt(2, 4), list(chunked_lines(new_woods_file(), 2))[1])

class TestParseArguments(unittest.TestCase):
    def test_args_no_space(self):
        from xin import parse_arguments

        args = '-L40 -P30 wc -l'.split(' ')
        args, command = parse_arguments(args)

        self.assertEquals(args['-L'], 40)
        self.assertEquals(args['-P'], 30)

    def test_args_no_command(self):
        from xin import parse_arguments

        args = '-L40 -P 30'.split(' ')

        with self.assertRaises(Exception):
            parse_arguments(args)

    def test_args_no_args(self):
        from xin import parse_arguments

        args = 'wc -l'.split(' ')
        args, command = parse_arguments(args)

        self.assertEquals(command, ['wc', '-l'])

    def test_args_integer_parameter(self):
        from xin import parse_arguments, InvalidArgumentException

        args = '-L FOO'.split(' ')

        with self.assertRaises(InvalidArgumentException):
            parse_arguments(args)

    def test_args_boolean(self):
        from xin import parse_arguments

        args = '-B wc -l'.split(' ')
        args, command = parse_arguments(args)

        self.assertTrue(args['-B'])

        args = 'wc -l'.split(' ')
        args, command = parse_arguments(args)

        self.assertFalse(args['-B'])

    def test_invalid_command(self):
        from xin import parse_arguments

        args = '-Z -l'.split(' ')

        with self.assertRaises(Exception):
            parse_arguments(args)
