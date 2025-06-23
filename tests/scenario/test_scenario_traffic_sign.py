import unittest

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_traffic_sign import (
    TrafficSignNoRightOfWay,
    TrafficSignRightOfWay,
    TrafficSignSpeedLimit,
    TrafficSignStopLine,
    TrafficSignTrafficLight,
)
from commonroad_labeling.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios


class ScenarioTrafficSignTest(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_scenarios()

    def test_traffic_sign_speed_limit(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_TRAFFIC_SIGN_SPEED_LIMIT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    TrafficSignSpeedLimit(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    TrafficSignSpeedLimit(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_traffic_right_of_way(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_TRAFFIC_SIGN_RIGHT_OF_WAY in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    TrafficSignRightOfWay(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    TrafficSignRightOfWay(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_traffic_no_right_of_way(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_TRAFFIC_SIGN_NO_RIGHT_OF_WAY in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    TrafficSignNoRightOfWay(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    TrafficSignNoRightOfWay(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_traffic_stop_line(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_TRAFFIC_SIGN_STOP_LINE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    TrafficSignStopLine(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )
            else:
                self.assertFalse(
                    TrafficSignStopLine(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )

    def test_traffic_traffic_light(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_TRAFFIC_SIGN_TRAFFIC_LIGHT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    TrafficSignTrafficLight(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    TrafficSignTrafficLight(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
