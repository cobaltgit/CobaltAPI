# Cobalt API

An unfinished, general purpose API with versatility in mind  
A public instance of this API will be available soon  

## Endpoints

`GET /fact?count={count}`  
Get random facts from a list of 3,090 facts  
`count` - optional parameter - the number of facts to retrieve - can be anywhere between 1 and 3090 (default: 1)

## Install your own instance

You'll need Git, Python 3.10+ and Poetry installed for this

* Clone this Git repository

```bash
$ git clone https://github.com/cobaltgit/CobaltAPI.git
```

* Install dependencies\* with Poetry

```bash
$ poetry install
```

\* to install development dependencies, do `poetry install --dev`

* Create the config file

```bash
$ mv config.example.json config.json
```

To run your instance on a different host or port, or to enable hot reload or hide the access logs, just manipulate the `config.json` file - the start script will handle the rest  
The number of workers will scale to the number of CPU threads available on your system, as per Gunicorn's recommendations (`nproc * 2 + 1`) - for example, a virtual machine with 2 CPU threads will run 5 workers

* Serve it up!

```bash
$ python3.10 run.py
```
