import os
import xml.etree.ElementTree as ET

from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.scenario.scenario import Scenario
from commonroad.visualization.mp_renderer import MPRenderer
from matplotlib import pyplot as plt

from commonroad_labeling.common.tag import Tag, TagGroup
from commonroad_labeling.road_configuration.lanelet_layout import LaneletLayoutLabeling
from commonroad_labeling.road_configuration.traffic_sign import TrafficSignLabeling


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
            scenario_xml = ET.parse(os.path.join(path, filename))
            root = scenario_xml.getroot()
            if root.tag == "commonRoad":
                new_tags = find_scenario_tags(os.path.join(path, filename))
                print(('{0:-<50}'.format(filename + ":  ") + "------ "),
                      list(map(lambda tag: Tag(tag).value, new_tags)))


def find_scenario_tags(path_to_file: str) -> set[Tag]:
    scenario = load_scenario(path_to_file)

    scenario_tags = set()
    for tagGroup in TagGroup:
        detected_tags = set()
        if TagGroup(tagGroup).value == TagGroup.TRAFFIC_SIGN:
            detected_tags = TrafficSignLabeling(scenario).get_tags_contained_in_scenario()
        elif TagGroup(tagGroup).value == TagGroup.LANELET_LAYOUT:
            detected_tags = LaneletLayoutLabeling(scenario).get_tags_contained_in_scenario()

        scenario_tags.update(detected_tags)

    return scenario_tags
