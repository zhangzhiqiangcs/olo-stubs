from setuptools import setup
import os

name = 'olo-stubs'
description = 'olo stubs and mypy plugin'

install_instructions = """\
# olo type stubs and mypy plugin

## Installation

```
pip install olo-stubs
```

Important: you need to enable the plugin in your mypy config file:
```
[mypy]
plugins = olomypy
```
"""


def find_stub_files():
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith('.pyi'):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


setup(name='olo-stubs',
      version='0.1',
      description=description,
      long_description=install_instructions,
      long_description_content_type='text/markdown',
      author='yetone',
      author_email='yetoneful@gmail.com',
      license='MIT License',
      url="https://github.com/yetone/olo-stubs",
      py_modules=['olomypy', 'olotyping'],
      install_requires=[
          'mypy>=0.720',
          'typing-extensions>=3.7.4'
      ],
      packages=['olo-stubs'],
      package_data={'olo-stubs': find_stub_files()},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3'
      ]
)
