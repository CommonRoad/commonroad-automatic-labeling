import unittest

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.ego_vehicle_goal.ego_vehicle_goal_intersection import (
    EgoVehicleGoalIntersectionProceedStraight,
    EgoVehicleGoalIntersectionTurnLeft,
    EgoVehicleGoalIntersectionTurnRight,
)
from commonroad_labeling.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios_with_routes


class EgoVehicleGoalIntersectionTest(unittest.TestCase):
    def setUp(self):
        self.scenarios_and_routes = get_scenarios_with_routes()

    def test_intersection_turn_left(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = EgoVehicleGoalIntersectionTurnLeft(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.EGO_VEHICLE_GOAL_INTERSECTION_TURN_LEFT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_intersection_turn_right(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = EgoVehicleGoalIntersectionTurnRight(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.EGO_VEHICLE_GOAL_INTERSECTION_TURN_RIGHT in expected_scenario_tags.get(
                str(scenario.scenario_id)
            ):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))

    def test_intersection_proceed_straight(self):
        for scenario, routes in self.scenarios_and_routes:
            is_fulfilled = None
            for route in routes:
                is_fulfilled = EgoVehicleGoalIntersectionProceedStraight(route).is_fulfilled()
                if is_fulfilled:
                    break

            if TagEnum.EGO_VEHICLE_GOAL_INTERSECTION_PROCEED_STRAIGHT in expected_scenario_tags.get(
                str(scenario.scenario_id)
            ):
                self.assertTrue(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
            else:
                self.assertFalse(is_fulfilled, msg=get_scenario_for_error(str(scenario.scenario_id)))
