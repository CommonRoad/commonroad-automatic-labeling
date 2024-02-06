import enum
from abc import ABC, abstractmethod

from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.scenario import Scenario
from commonroad.scenario.traffic_sign import TrafficSignIDZamunda, TrafficSignIDGermany, TrafficSignIDUsa, \
    TrafficSignIDChina, TrafficSignIDSpain, TrafficSignIDRussia, TrafficSignIDArgentina, TrafficSignIDBelgium, \
    TrafficSignIDFrance, TrafficSignIDGreece, TrafficSignIDCroatia, TrafficSignIDItaly, TrafficSignIDPuertoRico

from commonroad_labeling.common.tag import Tag, TagEnum


class TrafficSign(Tag, ABC):
    def is_fulfilled(self) -> bool:
        traffic_sign_ids = self.get_traffic_signs()
        for traffic_sign in self.scenario.lanelet_network.traffic_signs:
            for traffic_sign_id in traffic_sign_ids:
                if traffic_sign_id in list(
                        map(lambda traffic_sign_element: traffic_sign_element.traffic_sign_element_id,
                            traffic_sign.traffic_sign_elements)):
                    return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        traffic_sign_ids = self.get_traffic_signs()
        for lanelet_traffic_sign_id in lanelet.traffic_signs:
            if lanelet_traffic_sign_id in traffic_sign_ids:
                return True
        return False

    @abstractmethod
    def get_traffic_signs(self) -> list[enum]:
        pass


class TrafficSignSpeedLimit(TrafficSign):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.TRAFFIC_SIGN_SPEED_LIMIT

    def get_traffic_signs(self) -> list[enum]:
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

                # TODO: verify interstates, highways and expressways
                ]


class TrafficSignRightOfWay(TrafficSign):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.TRAFFIC_SIGN_RIGHT_OF_WAY

    def get_traffic_signs(self) -> list[enum]:
        return [
            TrafficSignIDZamunda.RIGHT_OF_WAY,
            TrafficSignIDGermany.RIGHT_OF_WAY,

            TrafficSignIDZamunda.PRIORITY,
            TrafficSignIDGermany.PRIORITY,

            TrafficSignIDZamunda.PRIORITY_OVER_ONCOMING,
            TrafficSignIDGermany.PRIORITY_OVER_ONCOMING,
        ]


class TrafficSignNoRightOfWay(TrafficSign):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.TRAFFIC_SIGN_NO_RIGHT_OF_WAY

    def get_traffic_signs(self) -> list[enum]:
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

            # TrafficSignIDZamunda.PEDESTRIAN_AND_BICYCLE_ROAD,
            # TrafficSignIDGermany.PEDESTRIAN_AND_BICYCLE_ROAD,

            # TrafficSignIDZamunda.BICYCLE_ROAD_START,
            # TrafficSignIDGermany.BICYCLE_ROAD_START,

            # TrafficSignIDZamunda.BICYCLE_ROAD_END,
            # TrafficSignIDGermany.BICYCLE_ROAD_END,

            TrafficSignIDZamunda.RAILWAY,
            TrafficSignIDGermany.RAILWAY,
        ]


class TrafficSignStopLine(Tag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.TRAFFIC_SIGN_STOP_LINE

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        return lanelet.stop_line is not None


class TrafficSignTrafficLight(Tag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.TRAFFIC_SIGN_TRAFFIC_LIGHT

    def is_fulfilled(self) -> bool:
        return len(self.scenario.lanelet_network.traffic_lights) > 0

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        return len(lanelet.traffic_lights) > 0
