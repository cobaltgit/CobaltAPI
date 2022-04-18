# Cobalt API

An unfinished, minimalistic, general purpose API with versatility in mind.

Public instance: [https://api.cobaltonline.net/](https://api.cobaltonline.net/)

## Endpoints

See `/` for a list of endpoints.

## Install your own instance

You'll need Git, Python 3.8+, and Poetry installed for this.

- 1. Clone this Git repository

```bash
git clone https://github.com/cobaltgit/CobaltAPI.git
```

- 2. Install dependencies\* with Poetry

```bash
poetry install
```

\* *to install development dependencies, do `poetry install --dev`*

- 3. Modify the `settings.py` file

To run your instance on a different host, port, turn off debug mode, etc... just manipulate the `settings.py` file - the start script will handle the rest.

`private_settings.py` contains sensitive information that should not be committed to the Git repository. You can copy its template and adjust it to your needs.

The number of workers will scale to the number of CPU threads available on your system, as per Gunicorn's recommendations (`nproc * 2 + 1`) - for example, a virtual machine with 2 CPU threads will run 5 workers.

- 4. Serve it up!

```bash
python3.10 run.py
```
