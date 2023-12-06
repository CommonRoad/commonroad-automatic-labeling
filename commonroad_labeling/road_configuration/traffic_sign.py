import enum

from commonroad.scenario.scenario import Scenario
from commonroad.scenario.traffic_sign import TrafficSignIDGermany, TrafficSignIDZamunda, TrafficSignIDUsa, \
    TrafficSignIDChina, TrafficSignIDSpain, TrafficSignIDRussia, TrafficSignIDArgentina, TrafficSignIDBelgium, \
    TrafficSignIDFrance, TrafficSignIDGreece, TrafficSignIDCroatia, TrafficSignIDItaly, TrafficSignIDPuertoRico

from commonroad_labeling.common.base import AutoLabelingBase
from commonroad_labeling.common.tag import Tag, TagGroup


class TrafficSignLabeling(AutoLabelingBase):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag_group = TagGroup.TRAFFIC_SIGN

    def scenario_contains_tag(self, tag: Tag) -> bool:
        if Tag(tag) == Tag.TRAFFIC_SIGN_SPEED_LIMIT:
            return self.contains_speed_limit()
        elif Tag(tag) == Tag.TRAFFIC_SIGN_TRAFFIC_LIGHT:
            return self.contains_traffic_light()
        return False

    def contains_speed_limit(self) -> bool:
        traffic_sign_ids = self.get_traffic_sign_ids_by_tag(Tag.TRAFFIC_SIGN_SPEED_LIMIT)
        for traffic_sign in self.scenario.lanelet_network.traffic_signs:
            for traffic_sign_id in traffic_sign_ids:
                if traffic_sign_id in list(
                        map(lambda traffic_sign_element: traffic_sign_element.traffic_sign_element_id,
                            traffic_sign.traffic_sign_elements)):
                    return True
        return False

    def contains_traffic_light(self) -> bool:
        return len(self.scenario.lanelet_network.traffic_lights) > 0

    @staticmethod
    def get_traffic_sign_ids_by_tag(tag: Tag) -> list[enum]:
        # TODO: resolve traffic signs depending on the tag
        if tag == Tag.TRAFFIC_SIGN_SPEED_LIMIT:
            return [TrafficSignIDZamunda.MAX_SPEED,
                    TrafficSignIDGermany.MAX_SPEED,
                    TrafficSignIDUsa.MAX_SPEED,
                    TrafficSignIDChina.MAX_SPEED,
                    TrafficSignIDSpain.MAX_SPEED,
                    TrafficSignIDRussia.MAX_SPEED,
                    TrafficSignIDArgentina.MAX_SPEED,
                    TrafficSignIDBelgium.MAX_SPEED,
                    TrafficSignIDFrance.MAX_SPEED,
                    TrafficSignIDGreece.MAX_SPEED,
                    TrafficSignIDCroatia.MAX_SPEED,
                    TrafficSignIDItaly.MAX_SPEED,
                    TrafficSignIDPuertoRico.MAX_SPEED]
        return []
