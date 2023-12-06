import enum
from enum import Enum

from commonroad.scenario.scenario import Scenario

enum_delimiter = "|"

@enum.unique
class TagGroup(str, Enum):
    LANELET_LAYOUT = "lanelet_layout" + enum_delimiter
    TRAFFIC_SIGN = "traffic_sign" + enum_delimiter

@enum.unique
class Tag(str, Enum):
    LANELET_LAYOUT_SINGLE_LANE = TagGroup.LANELET_LAYOUT + "single_lane"
    LANELET_LAYOUT_MULTI_LANE = TagGroup.LANELET_LAYOUT + "multi_lane"
    LANELET_LAYOUT_BIDIRECTIONAL = TagGroup.LANELET_LAYOUT + "bidirectional"
    LANELET_LAYOUT_ONE_WAY = TagGroup.LANELET_LAYOUT + "one_way"
    LANELET_LAYOUT_INTERSECTION = TagGroup.LANELET_LAYOUT + "intersection"

    TRAFFIC_SIGN_SPEED_LIMIT = TagGroup.TRAFFIC_SIGN + "speed_limit"
    TRAFFIC_SIGN_TRAFFIC_LIGHT = TagGroup.TRAFFIC_SIGN + "traffic_light"


def scenario_contains_tag(scenario: Scenario, target_tag: Tag) -> bool:
    for tag in scenario.tags:
        if tag == target_tag:
            return True
    return False
