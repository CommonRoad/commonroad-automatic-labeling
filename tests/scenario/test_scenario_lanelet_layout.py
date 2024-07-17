import unittest

from commonroad_labeling.common.tag import TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_lanelet_layout import (
    LaneletLayoutBidirectional,
    LaneletLayoutDivergingLane,
    LaneletLayoutIntersection,
    LaneletLayoutMergingLane,
    LaneletLayoutMultiLane,
    LaneletLayoutOneWay,
    LaneletLayoutRoundabout,
    LaneletLayoutSingleLane,
)
from tests.util_tests import expected_scenario_tags, get_scenario_for_error, get_scenarios


class ScenarioLaneletLayoutTest(unittest.TestCase):
    def setUp(self):
        self.scenarios = get_scenarios()

    def test_lanelet_layout_single_lane(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_SINGLE_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutSingleLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutSingleLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_lanelet_layout_multi_lane(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_MULTI_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutMultiLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutMultiLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_lanelet_layout_bidirectional(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_BIDIRECTIONAL in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutBidirectional(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutBidirectional(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_lanelet_layout_one_way(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_ONE_WAY in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutOneWay(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )
            else:
                self.assertFalse(
                    LaneletLayoutOneWay(scenario).is_fulfilled(), msg=get_scenario_for_error(str(scenario.scenario_id))
                )

    def test_lanelet_layout_intersection(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_INTERSECTION in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutIntersection(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutIntersection(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_lanelet_layout_diverging_lane(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_DIVERGING_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutDivergingLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutDivergingLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_lanelet_layout_merging_lane(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_MERGING_LANE in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutMergingLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutMergingLane(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )

    def test_lanelet_layout_roundabout(self):
        for scenario in self.scenarios:
            if TagEnum.SCENARIO_LANELET_LAYOUT_ROUNDABOUT in expected_scenario_tags.get(str(scenario.scenario_id)):
                self.assertTrue(
                    LaneletLayoutRoundabout(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
            else:
                self.assertFalse(
                    LaneletLayoutRoundabout(scenario).is_fulfilled(),
                    msg=get_scenario_for_error(str(scenario.scenario_id)),
                )
