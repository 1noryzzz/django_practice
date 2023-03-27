import subprocess

"""
subprocess.check_output:

By default, all communication is in bytes, and therefore any "input"
should be bytes, and the return value will be bytes.  If in text mode,
any "input" should be a string, and the return value will be a string
decoded according to locale encoding, or by "encoding" if set. Text mode
is triggered by setting any of text, encoding, errors or universal_newlines.
"""


def run_code(code):
    try:
        output = subprocess.check_output(
            ["python", "-c", code],
            universal_newlines=True,
            stderr=subprocess.STDOUT,
            timeout=5,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = "Time Out"
    return output


code = """import time \r\ntime.sleep(6)"""
print(run_code(code))
