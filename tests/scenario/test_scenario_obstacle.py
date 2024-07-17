import unittest

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_obstacle import (
    ObstacleOtherDynamic,
    ObstacleStatic,
    ObstacleTraffic,
)
from commonroad_labeling.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios


class ScenarioObstacleTest(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_scenarios()

    def test_obstacle_traffic(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_OBSTACLE_TRAFFIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    ObstacleTraffic(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )
            else:
                self.assertFalse(
                    ObstacleTraffic(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )

    def test_obstacle_other_dynamic(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_OBSTACLE_OTHER_DYNAMIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    ObstacleOtherDynamic(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )
            else:
                self.assertFalse(
                    ObstacleOtherDynamic(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )

    def test_obstacle_static(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_OBSTACLE_STATIC in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    ObstacleStatic(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )
            else:
                self.assertFalse(
                    ObstacleStatic(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )
