<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

Mypy plugin and stubs for [OLO](https://github.com/yetone/olo) inspired by [sqlalchemy-stubs](https://github.com/dropbox/sqlalchemy-stubs)
====================================

[![Build Status](https://travis-ci.org/yetone/olo-stubs.svg?branch=master)](https://travis-ci.org/yetone/olo-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package contains [type stubs](https://www.python.org/dev/peps/pep-0561/) and a
[mypy plugin](https://mypy.readthedocs.io/en/latest/extending_mypy.html#extending-mypy-using-plugins)
to provide more precise static types and type inference for
[OLO framework](https://github.com/yetone/olo). A simple example:

```python
from olo import Model, Field

class BaseModel(Model):
    pass

class User(BaseModel):
    __table_name__ = 'users'
    id = Field(int, primary_key=True)
    name = Field(str)

user: User
reveal_type(user.id)  # N: Revealed type is 'builtins.int*'
reveal_type(User.name)  # N: Revealed type is 'olo.field.Field[builtins.str]'
```

## Installation
Install latest published version as:
```
pip install -U olo-stubs
```

*Important*: you need to enable the plugin in your mypy config file:
```
[mypy]
plugins = olomypy
```

To install the development version of the package:
```
git clone https://github.com/yetone/olo-stubs
cd olo-stubs
pip install -U .
```

## Development Setup

First, clone the repo and cd into it, like in _Installation_, then:
```
git submodule update --init --recursive
pip install -r dev-requirements.txt
```

Then, to run the tests, simply:
```
pytest
```
