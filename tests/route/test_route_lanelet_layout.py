import unittest

from commonroad_labeling.common.tag import TagEnum
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
from tests.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios_with_routes


class RouteLaneletLayoutTest(unittest.TestCase):
    def setUp(self):
        self.scenarios_and_routes = get_scenarios_with_routes()

    def test_lanelet_layout_single_lane(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutSingleLane(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_SINGLE_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_multi_lane(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutMultiLane(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_MULTI_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_bidirectional(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutBidirectional(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_BIDIRECTIONAL in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_one_way(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutOneWay(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_ONE_WAY in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_intersection(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutIntersection(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_INTERSECTION in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_diverging_lane(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutDivergingLane(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_DIVERGING_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_merging_lane(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutMergingLane(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_MERGING_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_lanelet_layout_roundabout(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = RouteLaneletLayoutRoundabout(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.ROUTE_LANELET_LAYOUT_ROUNDABOUT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
