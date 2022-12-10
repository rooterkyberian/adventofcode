# setup

Install pyenv, and then:

    pyenv exec python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

# add deps

    echo dep >> requirements.in
    pip-compile
    pip install -r requirements.txt
