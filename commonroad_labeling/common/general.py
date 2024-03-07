import os
from pathlib import Path

from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.planning.planning_problem import PlanningProblemSet
from commonroad.scenario.scenario import Scenario
from commonroad_route_planner.route import Route
from commonroad_route_planner.route_planner import RoutePlanner

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.road_configuration.ego_vehicle_goal.ego_vehicle_goal_intersection import (
    EgoVehicleGoalIntersectionProceedStraight,
    EgoVehicleGoalIntersectionTurnLeft,
    EgoVehicleGoalIntersectionTurnRight,
)
from commonroad_labeling.road_configuration.route.route_lanelet_layout import (
    RouteLaneletLayoutBidirectional,
    RouteLaneletLayoutDivergingLane,
    RouteLaneletLayoutIntersection,
    RouteLaneletLayoutMergingLane,
    RouteLaneletLayoutMultiLane,
    RouteLaneletLayoutOneWay,
    RouteLaneletLayoutRoundabout,
    RouteLaneletLayoutSingleLane,
)
from commonroad_labeling.road_configuration.route.route_obstacle import (
    RouteObstacleOtherDynamic,
    RouteObstacleStatic,
    RouteOncomingTraffic,
    RouteTrafficAhead,
    RouteTrafficBehind,
)
from commonroad_labeling.road_configuration.route.route_traffic_sign import (
    RouteTrafficSignNoRightOfWay,
    RouteTrafficSignRightOfWay,
    RouteTrafficSignSpeedLimit,
    RouteTrafficSignStopLine,
    RouteTrafficSignTrafficLight,
)
from commonroad_labeling.road_configuration.scenario.scenario_lanelet_layout import (
    LaneletLayoutBidirectional,
    LaneletLayoutDivergingLane,
    LaneletLayoutIntersection,
    LaneletLayoutMergingLane,
    LaneletLayoutMultiLane,
    LaneletLayoutOneWay,
    LaneletLayoutRoundabout,
    LaneletLayoutSingleLane,
)
from commonroad_labeling.road_configuration.scenario.scenario_obstacle import (
    ObstacleOtherDynamic,
    ObstacleStatic,
    ObstacleTraffic,
)
from commonroad_labeling.road_configuration.scenario.scenario_traffic_sign import (
    TrafficSignNoRightOfWay,
    TrafficSignRightOfWay,
    TrafficSignSpeedLimit,
    TrafficSignStopLine,
    TrafficSignTrafficLight,
)


def go_through_dir(path: Path) -> None:
    if path.is_dir():
        for filename in os.listdir(path):
            new_path = path.joinpath(filename)
            if new_path.is_dir():
                go_through_dir(new_path)
            elif new_path.is_file() and new_path.suffix == ".xml":
                parse_file(new_path)
    elif path.is_file():
        parse_file(path)


def parse_file(path: Path):
    try:
        new_tags = find_scenario_tags(path)
        print(("{0:-<50}".format(path.name + ":  ") + "------ "), list(map(lambda tag: TagEnum(tag).value, new_tags)))
    except Exception as e:
        print(("{0:-<50}".format(path.name + ":  ") + "------ "), "Error parsing CommonRoad XML file:", e)


def get_planned_routes(scenario: Scenario, planning_problem_set: PlanningProblemSet) -> list[Route]:
    routes = []
    for planning_problem in list(planning_problem_set.planning_problem_dict.values()):
        route_planner = RoutePlanner(scenario, planning_problem, backend=RoutePlanner.Backend.NETWORKX_REVERSED)
        calculated_routes = route_planner.plan_routes().retrieve_all_routes()

        routes = [*routes, *(calculated_routes[0])]

    return routes


def find_scenario_tags(path_to_file: Path) -> set[TagEnum]:
    scenario, planning_problem_set = CommonRoadFileReader(path_to_file).open(lanelet_assignment=True)

    detected_tags = set()

    # Lanelet layout tags
    detected_tags.add(LaneletLayoutSingleLane(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutMultiLane(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutBidirectional(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutOneWay(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutIntersection(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutDivergingLane(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutMergingLane(scenario).get_tag_if_fulfilled())
    detected_tags.add(LaneletLayoutRoundabout(scenario).get_tag_if_fulfilled())

    # Obstacles tags
    detected_tags.add(ObstacleStatic(scenario).get_tag_if_fulfilled())
    detected_tags.add(ObstacleTraffic(scenario).get_tag_if_fulfilled())
    detected_tags.add(ObstacleOtherDynamic(scenario).get_tag_if_fulfilled())

    # Traffic sign tags
    detected_tags.add(TrafficSignSpeedLimit(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignRightOfWay(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignNoRightOfWay(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignStopLine(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignTrafficLight(scenario).get_tag_if_fulfilled())

    # Route tags
    routes = get_planned_routes(scenario, planning_problem_set)

    for route in routes:
        # Route lanelet layout tags
        detected_tags.add(RouteLaneletLayoutSingleLane(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutMultiLane(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutBidirectional(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutOneWay(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutIntersection(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutDivergingLane(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutMergingLane(route).get_tag_if_fulfilled())
        detected_tags.add(RouteLaneletLayoutRoundabout(route).get_tag_if_fulfilled())

        # Obstacles tags
        detected_tags.add(RouteObstacleStatic(route).get_tag_if_fulfilled())
        detected_tags.add(RouteObstacleOtherDynamic(route).get_tag_if_fulfilled())
        detected_tags.add(RouteTrafficAhead(route).get_tag_if_fulfilled())
        detected_tags.add(RouteTrafficBehind(route).get_tag_if_fulfilled())
        detected_tags.add(RouteOncomingTraffic(route).get_tag_if_fulfilled())

        # Traffic sign tags
        detected_tags.add(RouteTrafficSignSpeedLimit(route).get_tag_if_fulfilled())
        detected_tags.add(RouteTrafficSignRightOfWay(route).get_tag_if_fulfilled())
        detected_tags.add(RouteTrafficSignNoRightOfWay(route).get_tag_if_fulfilled())
        detected_tags.add(RouteTrafficSignStopLine(route).get_tag_if_fulfilled())
        detected_tags.add(RouteTrafficSignTrafficLight(route).get_tag_if_fulfilled())

        # Ego vehicle goal tags
        detected_tags.add(EgoVehicleGoalIntersectionTurnLeft(route).get_tag_if_fulfilled())
        detected_tags.add(EgoVehicleGoalIntersectionTurnRight(route).get_tag_if_fulfilled())
        detected_tags.add(EgoVehicleGoalIntersectionProceedStraight(route).get_tag_if_fulfilled())

    return set(filter(lambda tag: tag is not None, detected_tags))
