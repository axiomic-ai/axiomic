
import subprocess
import os

DIRNAME = os.path.dirname(__file__)

INPLACE = False

def run_notebook(filepath):
    # example command: jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 examples/tutorials/chat.ipynb
    if INPLACE:
        command = f'jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 {filepath}'
    else:
        # jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 --output {new_filepath} {original_filepath}
        new_filepath = '/tmp/output_notebook.ipynb'
        command = f'jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 --output {new_filepath} {filepath}'
    proc = subprocess.run(command, shell=True, cwd=DIRNAME)
    if proc.returncode != 0:
        raise Exception(f"Error running notebook: {filepath}")
    else:
        return True


def test_getting_started_notebook():
    path = 'tutorials/getting_started.ipynb'
    run_notebook(path)


def test_chat_notebook():
    path = 'tutorials/chat.ipynb'
    run_notebook(path)


def test_configure_notebook():
    path = 'tutorials/models.ipynb'
    run_notebook(path)


def test_graph_notebook():
    path = 'tutorials/graphs.ipynb'
    run_notebook(path)

