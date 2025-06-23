import unittest

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.road_configuration.route.route_traffic_sign import (
    RouteTrafficSignNoRightOfWay,
    RouteTrafficSignRightOfWay,
    RouteTrafficSignSpeedLimit,
    RouteTrafficSignStopLine,
    RouteTrafficSignTrafficLight,
)
from commonroad_labeling.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios_with_routes


class RouteTrafficSignTest(unittest.TestCase):
    def setUp(self):
        self.scenarios_and_routes = get_scenarios_with_routes()

    def test_traffic_sign_speed_limit(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficSignSpeedLimit(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_TRAFFIC_SIGN_SPEED_LIMIT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_traffic_right_of_way(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficSignRightOfWay(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_TRAFFIC_SIGN_RIGHT_OF_WAY in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_traffic_no_right_of_way(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficSignNoRightOfWay(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_TRAFFIC_SIGN_NO_RIGHT_OF_WAY in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_traffic_stop_line(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficSignStopLine(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_TRAFFIC_SIGN_STOP_LINE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_traffic_traffic_light(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficSignTrafficLight(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_TRAFFIC_SIGN_TRAFFIC_LIGHT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
