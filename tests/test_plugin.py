import subprocess
from textwrap import dedent


def test_actual_code(tmpdir):
    file = tmpdir / 'code.py'
    with file.open('w') as f:
        f.write(
            dedent(
                r"""
                x = 'hello\nworld'
                x = 'a\\b\nc\\d'
                x = 'C:\\Users\\root'
                x = '\\'
                x = r'C:\Users\root'
                """
            ).lstrip()
        )
    output = (
        subprocess.run(['poetry', 'run', 'flake8', str(file)], stdout=subprocess.PIPE)
        .stdout.decode()
        .strip()
    )
    assert output == (
        f'{tmpdir}/code.py:3:5: ' f'STR001 Unnecessary use of backslash escaping'
    )
