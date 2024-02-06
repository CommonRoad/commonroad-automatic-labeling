import enum
from abc import ABC, abstractmethod
from enum import Enum

from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.scenario import Scenario

enum_delimiter = "|"


@enum.unique
class TagGroupEnum(str, Enum):
    LANELET_LAYOUT = "lanelet_layout" + enum_delimiter
    TRAFFIC_SIGN = "traffic_sign" + enum_delimiter
    OBSTACLE = "obstacle" + enum_delimiter


@enum.unique
class TagEnum(str, Enum):
    LANELET_LAYOUT_SINGLE_LANE = TagGroupEnum.LANELET_LAYOUT + "single_lane"
    LANELET_LAYOUT_MULTI_LANE = TagGroupEnum.LANELET_LAYOUT + "multi_lane"
    LANELET_LAYOUT_BIDIRECTIONAL = TagGroupEnum.LANELET_LAYOUT + "bidirectional"
    LANELET_LAYOUT_ONE_WAY = TagGroupEnum.LANELET_LAYOUT + "one_way"
    LANELET_LAYOUT_INTERSECTION = TagGroupEnum.LANELET_LAYOUT + "intersection"
    LANELET_LAYOUT_DIVERGING_LANE = TagGroupEnum.LANELET_LAYOUT + "diverging_lane"
    LANELET_LAYOUT_MERGING_LANE = TagGroupEnum.LANELET_LAYOUT + "merging_lane"
    LANELET_LAYOUT_ROUNDABOUT = TagGroupEnum.LANELET_LAYOUT + "roundabout"

    TRAFFIC_SIGN_SPEED_LIMIT = TagGroupEnum.TRAFFIC_SIGN + "speed_limit"
    TRAFFIC_SIGN_RIGHT_OF_WAY = TagGroupEnum.TRAFFIC_SIGN + "right_of_way"
    TRAFFIC_SIGN_NO_RIGHT_OF_WAY = TagGroupEnum.TRAFFIC_SIGN + "no_right_of_way"
    TRAFFIC_SIGN_STOP_LINE = TagGroupEnum.TRAFFIC_SIGN + "stop_line"
    TRAFFIC_SIGN_TRAFFIC_LIGHT = TagGroupEnum.TRAFFIC_SIGN + "traffic_light"

    OBSTACLE_ONCOMING_TRAFFIC = TagGroupEnum.OBSTACLE + "oncoming_traffic"
    OBSTACLE_NO_ONCOMING_TRAFFIC = TagGroupEnum.OBSTACLE + "no_oncoming_traffic"
    OBSTACLE_TRAFFIC_AHEAD = TagGroupEnum.OBSTACLE + "traffic_ahead"
    OBSTACLE_TRAFFIC_BEHIND = TagGroupEnum.OBSTACLE + "traffic_behind"
    OBSTACLE_TRAFFIC_AROUND = TagGroupEnum.OBSTACLE + "traffic_around"
    OBSTACLE_OTHER_DYNAMIC = TagGroupEnum.OBSTACLE + "other_dynamic"
    OBSTACLE_STATIC = TagGroupEnum.OBSTACLE + "static"


class Tag(ABC):
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.tag = None

    def get_tag_if_fulfilled(self) -> TagEnum | None:
        if self.is_fulfilled():
            return self.tag
        return None

    @abstractmethod
    def is_fulfilled(self) -> bool:
        pass

    @abstractmethod
    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        pass
