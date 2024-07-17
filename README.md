# Automatic Scenario Labeling
[![pipeline status](https://gitlab.lrz.de/cps/commonroad/automatic-scenario-labeling/badges/develop/pipeline.svg)](https://gitlab.lrz.de/cps/commonroad/automatic-scenario-labeling/-/commits/develop)
[![coverage report](https://gitlab.lrz.de/cps/commonroad/automatic-scenario-labeling/badges/develop/coverage.svg)](https://gitlab.lrz.de/cps/commonroad/automatic-scenario-labeling/-/commits/develop)

## Intended Functionality
This tool aims to automatically assign the correct labels to CommonRoad scenarios.

The full list of available labels in CommonRoad is:
Comfort, Critical, Emergency Breaking, Evasive, Highway, Illegal Cut In, Intersection, Interstate, Lane Change, Lane Following, Merging Lanes, Multi Lane, No Oncoming Traffic, Oncoming Traffic, Parallel Lanes, Race Track, Roundabout, Rural, Simulated, Single Lane, Slip Road, Speed Limit, Traffic Jam, Turn Left, Turn Right, Two Lane, Urban

## Sketched Functionality
1. Load scenario using commonroad-io.
2. Read all currently assigned scenario tags.
3. Determine which tags are correct.
   1. Using formalized rules.
   2. Using traffic rule monitor.
   3. Using criticality metrics.
4. Check whether the tags are consistent with the previously assigned tags. → Warning if necessary
5. Overwrite scenario with corrected tags.

## Fulfill Conventions
- Well documented code.
- Use Poetry.
- Use CI/CD.
- Stick to coding conventions (use linting).
- Providing a version-stable Docker file.
