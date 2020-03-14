import contextlib
from textwrap import dedent

from flake8_plugin_utils import utils
from flake8_strings.errors import UnnecessaryBackslashEscapingError
from flake8_strings.visitor import StringsVisitor


@contextlib.contextmanager
def setup_visitor_class(visitor, code):
    visitor.lines = code.splitlines()
    yield
    delattr(visitor, 'lines')


def assert_error(visitor, code, error, config=None, **kwargs):
    with setup_visitor_class(visitor, code):
        utils.assert_error(visitor, code, error, config, **kwargs)


def assert_not_error(visitor, code, config=None):
    with setup_visitor_class(visitor, code):
        utils.assert_not_error(visitor, code, config=config)


def test_error():
    code = dedent(r"""x = 'C:\\Users\\root\\Documents'""")
    assert_error(StringsVisitor, code, UnnecessaryBackslashEscapingError)


def test_no_error():
    code = dedent(r"""x = 'hello\nworld, x\\y'""")
    assert_not_error(StringsVisitor, code)


def test_no_error_raw_string():
    code = dedent(r"""x = r'C:\User\root'""")
    assert_not_error(StringsVisitor, code)
