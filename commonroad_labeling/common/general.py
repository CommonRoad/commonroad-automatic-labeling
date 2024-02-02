import os
import xml.etree.ElementTree as ET

from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.tag import TagEnum, TagGroupEnum
from commonroad_labeling.road_configuration.lanelet_layout import LaneletLayoutSingleLane, LaneletLayoutMultiLane, \
    LaneletLayoutBidirectional, LaneletLayoutOneWay, LaneletLayoutIntersection, LaneletLayoutDivergingLane, \
    LaneletLayoutMergingLane, LaneletLayoutRoundabout
from commonroad_labeling.road_configuration.obstacle import ObstacleStatic
from commonroad_labeling.road_configuration.traffic_sign import TrafficSignSpeedLimit, TrafficSignRightOfWay, \
    TrafficSignNoRightOfWay, TrafficSignTrafficLight


def load_scenario(path: str) -> Scenario:
    scenario, _ = CommonRoadFileReader(path).open(
        lanelet_assignment=True
    )

    return scenario


def go_through_dir(path: str) -> None:
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            go_through_dir(os.path.join(path, filename))
        elif os.path.isfile(os.path.join(path, filename)) and filename.endswith(".xml"):
            # check if scenario is a commonRoad file
            scenario_xml = ET.parse(os.path.join(path, filename))
            root = scenario_xml.getroot()
            if root.tag == "commonRoad":
                new_tags = find_scenario_tags(os.path.join(path, filename))
                print(('{0:-<50}'.format(filename + ":  ") + "------ "),
                      list(map(lambda tag: TagEnum(tag).value, new_tags)))
            else:
                print("File is not a CommonRoad XML file")


def find_scenario_tags(path_to_file: str) -> set[TagEnum]:
    scenario = load_scenario(path_to_file)

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

    # Traffic sign tags
    detected_tags.add(TrafficSignSpeedLimit(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignRightOfWay(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignNoRightOfWay(scenario).get_tag_if_fulfilled())
    detected_tags.add(TrafficSignTrafficLight(scenario).get_tag_if_fulfilled())

    return set(filter(lambda tag: tag is not None, detected_tags))
