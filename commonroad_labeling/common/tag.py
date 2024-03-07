import enum
from abc import ABC, abstractmethod
from enum import Enum

from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.scenario import Scenario
from commonroad_route_planner.route import Route

enum_delimiter = "|"


@enum.unique
class TagGroupEnum(str, Enum):
    SCENARIO_LANELET_LAYOUT = "scenario_lanelet_layout" + enum_delimiter
    SCENARIO_TRAFFIC_SIGN = "scenario_traffic_sign" + enum_delimiter
    SCENARIO_OBSTACLE = "scenario_obstacle" + enum_delimiter

    ROUTE_LANELET_LAYOUT = "ego_vehicle_route_lanelet_layout" + enum_delimiter
    ROUTE_TRAFFIC_SIGN = "ego_vehicle_route_traffic_sign" + enum_delimiter
    ROUTE_OBSTACLE = "ego_vehicle_route_obstacle" + enum_delimiter

    EGO_VEHICLE_GOAL_INTERSECTION = "ego_vehicle_goal_intersection" + enum_delimiter


@enum.unique
class TagEnum(str, Enum):
    SCENARIO_LANELET_LAYOUT_SINGLE_LANE = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "single_lane"
    SCENARIO_LANELET_LAYOUT_MULTI_LANE = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "multi_lane"
    SCENARIO_LANELET_LAYOUT_BIDIRECTIONAL = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "bidirectional"
    SCENARIO_LANELET_LAYOUT_ONE_WAY = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "one_way"
    SCENARIO_LANELET_LAYOUT_INTERSECTION = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "intersection"
    SCENARIO_LANELET_LAYOUT_DIVERGING_LANE = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "diverging_lane"
    SCENARIO_LANELET_LAYOUT_MERGING_LANE = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "merging_lane"
    SCENARIO_LANELET_LAYOUT_ROUNDABOUT = TagGroupEnum.SCENARIO_LANELET_LAYOUT + "roundabout"

    SCENARIO_TRAFFIC_SIGN_SPEED_LIMIT = TagGroupEnum.SCENARIO_TRAFFIC_SIGN + "speed_limit"
    SCENARIO_TRAFFIC_SIGN_RIGHT_OF_WAY = TagGroupEnum.SCENARIO_TRAFFIC_SIGN + "right_of_way"
    SCENARIO_TRAFFIC_SIGN_NO_RIGHT_OF_WAY = TagGroupEnum.SCENARIO_TRAFFIC_SIGN + "no_right_of_way"
    SCENARIO_TRAFFIC_SIGN_STOP_LINE = TagGroupEnum.SCENARIO_TRAFFIC_SIGN + "stop_line"
    SCENARIO_TRAFFIC_SIGN_TRAFFIC_LIGHT = TagGroupEnum.SCENARIO_TRAFFIC_SIGN + "traffic_light"

    SCENARIO_OBSTACLE_TRAFFIC = TagGroupEnum.SCENARIO_OBSTACLE + "traffic"
    SCENARIO_OBSTACLE_OTHER_DYNAMIC = TagGroupEnum.SCENARIO_OBSTACLE + "other_dynamic"
    SCENARIO_OBSTACLE_STATIC = TagGroupEnum.SCENARIO_OBSTACLE + "static"

    ROUTE_LANELET_LAYOUT_SINGLE_LANE = TagGroupEnum.ROUTE_LANELET_LAYOUT + "single_lane"
    ROUTE_LANELET_LAYOUT_MULTI_LANE = TagGroupEnum.ROUTE_LANELET_LAYOUT + "multi_lane"
    ROUTE_LANELET_LAYOUT_BIDIRECTIONAL = TagGroupEnum.ROUTE_LANELET_LAYOUT + "bidirectional"
    ROUTE_LANELET_LAYOUT_ONE_WAY = TagGroupEnum.ROUTE_LANELET_LAYOUT + "one_way"
    ROUTE_LANELET_LAYOUT_INTERSECTION = TagGroupEnum.ROUTE_LANELET_LAYOUT + "intersection"
    ROUTE_LANELET_LAYOUT_DIVERGING_LANE = TagGroupEnum.ROUTE_LANELET_LAYOUT + "diverging_lane"
    ROUTE_LANELET_LAYOUT_MERGING_LANE = TagGroupEnum.ROUTE_LANELET_LAYOUT + "merging_lane"
    ROUTE_LANELET_LAYOUT_ROUNDABOUT = TagGroupEnum.ROUTE_LANELET_LAYOUT + "roundabout"

    ROUTE_TRAFFIC_SIGN_SPEED_LIMIT = TagGroupEnum.ROUTE_TRAFFIC_SIGN + "speed_limit"
    ROUTE_TRAFFIC_SIGN_RIGHT_OF_WAY = TagGroupEnum.ROUTE_TRAFFIC_SIGN + "right_of_way"
    ROUTE_TRAFFIC_SIGN_NO_RIGHT_OF_WAY = TagGroupEnum.ROUTE_TRAFFIC_SIGN + "no_right_of_way"
    ROUTE_TRAFFIC_SIGN_STOP_LINE = TagGroupEnum.ROUTE_TRAFFIC_SIGN + "stop_line"
    ROUTE_TRAFFIC_SIGN_TRAFFIC_LIGHT = TagGroupEnum.ROUTE_TRAFFIC_SIGN + "traffic_light"

    ROUTE_OBSTACLE_ONCOMING_TRAFFIC = TagGroupEnum.ROUTE_OBSTACLE + "oncoming_traffic"
    ROUTE_OBSTACLE_NO_ONCOMING_TRAFFIC = TagGroupEnum.ROUTE_OBSTACLE + "no_oncoming_traffic"
    ROUTE_OBSTACLE_TRAFFIC_AHEAD = TagGroupEnum.ROUTE_OBSTACLE + "traffic_ahead"
    ROUTE_OBSTACLE_TRAFFIC_BEHIND = TagGroupEnum.ROUTE_OBSTACLE + "traffic_behind"
    ROUTE_OBSTACLE_OTHER_DYNAMIC = TagGroupEnum.ROUTE_OBSTACLE + "other_dynamic"
    ROUTE_OBSTACLE_STATIC = TagGroupEnum.ROUTE_OBSTACLE + "static"

    EGO_VEHICLE_GOAL_INTERSECTION_TURN_LEFT = TagGroupEnum.EGO_VEHICLE_GOAL_INTERSECTION + "turn_left"
    EGO_VEHICLE_GOAL_INTERSECTION_TURN_RIGHT = TagGroupEnum.EGO_VEHICLE_GOAL_INTERSECTION + "turn_right"
    EGO_VEHICLE_GOAL_INTERSECTION_PROCEED_STRAIGHT = TagGroupEnum.EGO_VEHICLE_GOAL_INTERSECTION + "proceed_straight"


class Tag(ABC):
    def __init__(self):
        self.tag = None

    def get_tag_if_fulfilled(self) -> TagEnum | None:
        if self.is_fulfilled():
            return self.tag
        return None

    @abstractmethod
    def is_fulfilled(self) -> bool:
        pass


class ScenarioTag(Tag, ABC):
    def __init__(self, scenario: Scenario):
        self.scenario = scenario

    @abstractmethod
    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        pass


class RouteTag(Tag, ABC):
    def __init__(self, route: Route, scenario_tag: ScenarioTag):
        self.route = route
        self.scenario_tag = scenario_tag

    def get_route_lanelets(self) -> list[Lanelet]:
        return [
            self.route.lanelet_network.find_lanelet_by_id(lanelet_id) for lanelet_id in self.route.list_ids_lanelets
        ]

    def is_fulfilled(self) -> bool:
        lanelets = self.get_route_lanelets()
        for lanelet in lanelets:
            if self.scenario_tag.is_fulfilled_for_lanelet(lanelet):
                return True
        return False


class EgoVehicleGoal(Tag, ABC):
    def __init__(self, route: Route):
        self.route = route

    # TODO: future improvement - get actual vehicle path instead of the high level route
    def get_route_lanelets(self) -> list[Lanelet]:
        return [
            self.route.lanelet_network.find_lanelet_by_id(lanelet_id) for lanelet_id in self.route.list_ids_lanelets
        ]
