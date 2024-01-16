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
        traffic_sign_ids = TrafficSignLabeling.get_traffic_sign_ids_by_tag(Tag.TRAFFIC_SIGN_SPEED_LIMIT)
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
            return TrafficSignLabeling.get_speed_limit_traffic_signs()
        if tag == Tag.TRAFFIC_SIGN_RIGHT_OF_WAY:
            return TrafficSignLabeling.get_right_of_way_traffic_signs()
        if tag == Tag.TRAFFIC_SIGN_NO_RIGHT_OF_WAY:
            return TrafficSignLabeling.get_no_right_of_way_traffic_signs()
        return []

    @staticmethod
    def get_speed_limit_traffic_signs() -> list[enum]:
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
                TrafficSignIDPuertoRico.MAX_SPEED,

                TrafficSignIDZamunda.MAX_SPEED_ZONE_START,
                TrafficSignIDZamunda.MAX_SPEED_ZONE_START,

                TrafficSignIDZamunda.MAX_SPEED_ZONE_END,
                TrafficSignIDGermany.MAX_SPEED_ZONE_END,

                TrafficSignIDZamunda.MAX_SPEED_END,
                TrafficSignIDGermany.MAX_SPEED_END,

                TrafficSignIDZamunda.ALL_MAX_SPEED_AND_OVERTAKING_END,
                TrafficSignIDGermany.ALL_MAX_SPEED_AND_OVERTAKING_END,

                TrafficSignIDZamunda.MIN_SPEED,
                TrafficSignIDGermany.MIN_SPEED,

                TrafficSignIDZamunda.TOWN_SIGN,
                TrafficSignIDGermany.TOWN_SIGN,

                TrafficSignIDZamunda.TUNNEL,
                TrafficSignIDGermany.TUNNEL,
                # TODO: verify interstates, highways and expressways
                ]

    @staticmethod
    def get_right_of_way_traffic_signs() -> list[enum]:
        return [
            TrafficSignIDZamunda.RIGHT_OF_WAY,
            TrafficSignIDGermany.RIGHT_OF_WAY,

            TrafficSignIDZamunda.PRIORITY,
            TrafficSignIDGermany.PRIORITY,

            TrafficSignIDZamunda.PRIORITY_OVER_ONCOMING,
            TrafficSignIDGermany.PRIORITY_OVER_ONCOMING,
        ]

    @staticmethod
    def get_no_right_of_way_traffic_signs() -> list[enum]:
        return [
            TrafficSignIDZamunda.YIELD,
            TrafficSignIDGermany.YIELD,
            TrafficSignIDSpain.YIELD,

            TrafficSignIDZamunda.STOP,
            TrafficSignIDGermany.STOP,
            TrafficSignIDSpain.STOP,

            TrafficSignIDZamunda.PEDESTRIANS_CROSSING,
            TrafficSignIDGermany.PEDESTRIANS_CROSSING,
            TrafficSignIDSpain.PEDESTRIANS_CROSSING,

            TrafficSignIDZamunda.PRIORITY_OPPOSITE_DIRECTION,
            TrafficSignIDGermany.PRIORITY_OPPOSITE_DIRECTION,

            TrafficSignIDZamunda.ROUNDABOUT,
            TrafficSignIDGermany.ROUNDABOUT,

            TrafficSignIDZamunda.PEDESTRIAN_AND_BICYCLE_ROAD,
            TrafficSignIDGermany.PEDESTRIAN_AND_BICYCLE_ROAD,

            TrafficSignIDZamunda.PEDESTRIAN_ZONE_START,
            TrafficSignIDGermany.PEDESTRIAN_ZONE_START,

            TrafficSignIDZamunda.PEDESTRIAN_ZONE_END,
            TrafficSignIDGermany.PEDESTRIAN_ZONE_END,

            TrafficSignIDZamunda.BICYCLE_ROAD_START,
            TrafficSignIDGermany.BICYCLE_ROAD_START,

            TrafficSignIDZamunda.BICYCLE_ROAD_END,
            TrafficSignIDGermany.BICYCLE_ROAD_END,

            TrafficSignIDZamunda.RAILWAY,
            TrafficSignIDGermany.RAILWAY,
        ]

