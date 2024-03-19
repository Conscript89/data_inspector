# Data inspector


Data inspector is rather simple python tool designed to help with
inspecting various data files (initially json only) in a way that
helps construct python compatible expressions that could be used
directly in code.

The tool is focused only on filtering and showing data which is filtered
by provided expressions(s).

## Instructions to install/run the data inspector


### Fedora copr package

RPM packages are automatically built from the main branch in following
Fedora copr repository: https://copr.fedorainfracloud.org/coprs/conscript89/data_inspector/

To install the data inspector from this copr repository on your Fedora
system just run following commands:
```bash
dnf copr enable conscript89/data_inspector
dnf install data_inspector
```
Then just run:
```bash
data_inspector -h
```

### Python pip

The data inspector is also packaged (but currently not distributed on PyPy)
as pip compatible and can be installed by pip by running following command:
```bash
pip install https://github.com/Conscript89/data_inspector/archive/refs/heads/main.zip
```
Then just run:
```bash
data_inspector -h
```

### Python library without installation

The most direct way where you can have full control over the dependencies
is to just clone this repo, add the `src/data_inspector` to `PYTHONPATH`
and run the `data_inspector` module just like:
```bash
PYTHONPATH=$(pwd)/src python3 -m data_inspector -h
```

You're going to need to have the following python libraries installed:
 * textual
 * jinja2

Please consult the required dependencies with `pyproject.toml` which is
the source of truth and is used for all the packaging options.
