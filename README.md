# sqclib

Sqclib is a small python library used for interacting with the
[SQC](https://github.com/sb-ncbr/sqc) validation server.

## Installation

To install the latest version of the library, you can simply use pip. Make sure
you have an ssh key with access to the [SB-NCBR](https://github.com/sb-ncbr)
github organization. It is recommended to create a virtual environment first.
``` sh
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install git@github.com:sb-ncbr/sqclib.git
```

## Documentation
Until some kind of hosting solution is found, the docs must be built manually.
Clone the repository, create a virtual environment and install sphinx.
``` sh
$ git clone git@github.com:sb-ncbr/sqclib.git
$ cd sqclib
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install sphinx
```

Now from the project root directory, you can build the documentation.
``` sh
$ make -C docs html
```

The generated documentation can be accessed by opening the
`./docs/build/html/index.html` file in any browser.
