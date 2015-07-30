import unittest

class TestOutputResult(unittest.TestCase):
    def test_output_only_stdout(self):
        result = None

        from xin import output_result

    def test_output_only_stderr(self):
        pass

    def test_output_neither(self):
        pass

    def test_output_both(self):
        pass

class TestLineChunking(unittest.TestCase):
    def setUp(self):
        self.file = 'Foo\nBar\nBaz'

    def test_chunk_lines_default(self):
        pass

    def test_chunk_lines_size_n(self):
        pass

class TestParseArguments(unittest.TestCase):
    def test_args_no_space(self):
        pass

    def test_args_no_command(self):
        pass

    def test_args_no_args(self):
        pass

    def test_args_integer_parameter(self):
        pass

    def test_args_boolean(self):
        pass
