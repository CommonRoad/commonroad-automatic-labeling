# CommonRoad Automatic Scenario Labeling
The following code has been taken from the [CommonRoad Automatic Scenario Labeling repository](https://gitlab.lrz.de/cps/commonroad/automatic-scenario-labeling).

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/commonroad-prediction.svg)](https://pypi.python.org/pypi/commonroad-prediction/)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
[![PyPI version fury.io](https://badge.fury.io/py/commonroad-prediction.svg)](https://pypi.python.org/pypi/commonroad-prediction/)
[![PyPI license](https://img.shields.io/pypi/l/commonroad-prediction.svg)](https://pypi.python.org/pypi/commonroad-prediction/)

This is a tool that automatically detects CommonRoad scenario labels.

## Project status
Currently implemented and tested models:

- Static detection of CommonRoad scenario elements
- Dynamic detection of CommonRoad scenario elements that ego vehicle should encounter in high level planned routes
- Simple ego vehicle goal detections

In development:

-  Critical scenarios and expected ego vehicle behaviours


## Installation and Usage
We recommend using PyCharm (Professional) as IDE.
### Usage in other projects
We provide a PyPI package which can be installed with the following command
```shell
pip install commonroad-labeling
```

### Development
It is recommended to use [poetry](https://python-poetry.org/) as an environment manager.
Clone the repository and install it with poetry.
```shell
git clone git@gitlab.lrz.de:cps/commonroad/automatic-scenario-labeling.git
poetry shell
poetry install
```

### Examples
We recommend using PyCharm (Professional) as IDE.
An example script for detecting tags in a specified folder is [here](example.md).


## Documentation
You can generate the documentation within your activated Poetry environment using.
```bash
poetry shell
mkdocs build
```
The documentation will be located under site, where you can open `index.html` in your browser to view it.
For updating the documentation, you can also use the live preview:
```bash
poetry shell
mkdocs serve
```

## Authors
Responsible: Florian Finkeldei, Dzan Tabakovic
