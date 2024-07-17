import unittest

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.road_configuration.route.route_obstacle import (
    RouteObstacleOtherDynamic,
    RouteObstacleStatic,
    RouteOncomingTraffic,
    RouteTrafficAhead,
    RouteTrafficBehind,
)
from commonroad_labeling.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios_with_routes


class RouteObstacleTest(unittest.TestCase):
    def setUp(self):
        self.scenarios_and_routes = get_scenarios_with_routes()

    def test_obstacle_traffic_oncoming(self):
        for scenario, routes in self.scenarios_and_routes:
            detected_tags = set()
            for route in routes:
                detected_tags.add(RouteOncomingTraffic(route).get_tag_if_fulfilled())

            if TagEnum.ROUTE_OBSTACLE_ONCOMING_TRAFFIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertIn(
                    TagEnum.ROUTE_OBSTACLE_ONCOMING_TRAFFIC,
                    detected_tags,
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

            if TagEnum.ROUTE_OBSTACLE_NO_ONCOMING_TRAFFIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertIn(
                    TagEnum.ROUTE_OBSTACLE_NO_ONCOMING_TRAFFIC,
                    detected_tags,
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

            if TagEnum.ROUTE_OBSTACLE_NO_ONCOMING_TRAFFIC not in expected_scenario_tags.get(
                str(scenario.scenario_id)
            ) and TagEnum.ROUTE_OBSTACLE_ONCOMING_TRAFFIC not in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertNotIn(
                    TagEnum.ROUTE_OBSTACLE_NO_ONCOMING_TRAFFIC,
                    detected_tags,
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
                self.assertNotIn(
                    TagEnum.ROUTE_OBSTACLE_ONCOMING_TRAFFIC,
                    detected_tags,
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_obstacle_traffic_ahead(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficAhead(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_OBSTACLE_TRAFFIC_AHEAD in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_obstacle_traffic_behind(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteTrafficBehind(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_OBSTACLE_TRAFFIC_BEHIND in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_obstacle_other_dynamic(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteObstacleOtherDynamic(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_OBSTACLE_OTHER_DYNAMIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_obstacle_static(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteObstacleStatic(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_OBSTACLE_STATIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
