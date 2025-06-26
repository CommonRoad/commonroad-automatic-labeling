# CommonRoad Automatic Scenario Labeling

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/commonroad-labeling.svg)](https://pypi.python.org/pypi/commonroad-labeling/)
[![PyPI version fury.io](https://badge.fury.io/py/commonroad-labeling.svg)](https://pypi.python.org/pypi/commonroad-labeling/)
[![PyPI download week](https://img.shields.io/pypi/dw/commonroad-labeling.svg?label=PyPI%20downloads)](https://pypi.python.org/pypi/commonroad-labeling/)
[![PyPI download month](https://img.shields.io/pypi/dm/commonroad-labeling.svg?label=PyPI%20downloads)](https://pypi.python.org/pypi/commonroad-labeling/)
[![PyPI license](https://img.shields.io/pypi/l/commonroad-labeling.svg)](https://pypi.python.org/pypi/commonroad-labeling/)

Automatically assign correct labels to CommonRoad scenarios and check whether existing tags are correct.

## Project status

`commonroad-labeling` currently supports the following tags:
- Comfort
- Critical
- Emergency Breaking
- Evasive
- Highway
- Illegal Cut In
- Intersection
- Interstate
- Lane Change
- Lane Following
- Merging Lanes
- Multi Lane
- No Oncoming Traffic
- Oncoming Traffic
- Parallel Lanes
- Race Track
- Roundabout
- Rural
- Simulated
- Single Lane
- Slip Road
- Speed Limit
- Traffic Jam
- Turn Left
- Turn Right
- Two Lane
- Urban

Currently implemented and tested models:

- Static detection of CommonRoad scenario elements
- Dynamic detection of CommonRoad scenario elements that ego vehicle should encounter in high level planned routes
- Simple ego vehicle goal detections

In development:

- Critical scenarios and expected ego vehicle behaviours.

## Installation and Usage

We provide a PyPI package which can be installed with the following command:

```shell
pip install commonroad-labeling
```

### Examples
An example script for detecting tags in a specified folder is [here](example.md).



## Authors
Responsible: Florian Finkeldei, Dzan Tabakovic
