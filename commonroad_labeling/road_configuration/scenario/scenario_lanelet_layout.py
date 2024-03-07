from commonroad.scenario.intersection import Intersection
from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.tag import ScenarioTag, TagEnum


class LaneletLayoutSingleLane(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_SINGLE_LANE

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        if (lanelet.adj_left_same_direction is None or not lanelet.adj_left_same_direction) and (
            lanelet.adj_right_same_direction is None and not lanelet.adj_right_same_direction
        ):
            return True
        return False


class LaneletLayoutMultiLane(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_MULTI_LANE

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        if (lanelet.adj_left_same_direction is not None and lanelet.adj_left_same_direction) or (
            lanelet.adj_right_same_direction is not None and lanelet.adj_right_same_direction
        ):
            return True
        return False


class LaneletLayoutBidirectional(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_BIDIRECTIONAL

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        if (lanelet.adj_left_same_direction is not None and not lanelet.adj_left_same_direction) or (
            lanelet.adj_right_same_direction is not None and not lanelet.adj_right_same_direction
        ):
            return True
        return False


class LaneletLayoutOneWay(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_ONE_WAY

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        is_one_way = True
        if lanelet.adj_left_same_direction is None or lanelet.adj_left_same_direction:
            is_one_way = is_one_way and self.adj_lanelet_has_same_dir_neighbors_or_none(
                lanelet.adj_left, [lanelet.lanelet_id]
            )
        else:
            is_one_way = False

        if lanelet.adj_right_same_direction is None or lanelet.adj_right_same_direction:
            is_one_way = is_one_way and self.adj_lanelet_has_same_dir_neighbors_or_none(
                lanelet.adj_right, [lanelet.lanelet_id]
            )
        else:
            is_one_way = False

        if is_one_way:
            return True

        return False

    def adj_lanelet_has_same_dir_neighbors_or_none(self, lanelet_id: int, previous_lanelet_ids: list[int]) -> bool:
        if lanelet_id is None:
            return True
        for lanelet in self.scenario.lanelet_network.lanelets:
            if lanelet.lanelet_id == lanelet_id:
                is_one_way = True
                if lanelet.adj_left_same_direction is None or (
                    lanelet.adj_left not in previous_lanelet_ids and lanelet.adj_left_same_direction
                ):
                    is_one_way = is_one_way and self.adj_lanelet_has_same_dir_neighbors_or_none(
                        lanelet.adj_left, [*previous_lanelet_ids, lanelet.lanelet_id]
                    )
                elif lanelet.adj_left not in previous_lanelet_ids:
                    is_one_way = False

                if lanelet.adj_right_same_direction is None or (
                    lanelet.adj_right not in previous_lanelet_ids and lanelet.adj_right_same_direction
                ):
                    is_one_way = is_one_way and self.adj_lanelet_has_same_dir_neighbors_or_none(
                        lanelet.adj_right, [*previous_lanelet_ids, lanelet.lanelet_id]
                    )
                elif lanelet.adj_right not in previous_lanelet_ids:
                    is_one_way = False

                return is_one_way

        return True


class LaneletLayoutIntersection(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_INTERSECTION

    def is_fulfilled(self) -> bool:
        return len(self.scenario.lanelet_network.intersections) > 0

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        for intersection in self.scenario.lanelet_network.intersections:
            if lanelet.lanelet_id in self.get_intersection_lanelet_ids(intersection):
                return True
        return False

    def get_intersection_lanelet_ids(self, intersection: Intersection) -> set[int]:
        lanelets = set()
        for intersection_incoming in intersection.incomings:
            lanelets = lanelets.union(intersection_incoming.incoming_lanelets)
            if intersection_incoming.successors_left is not None:
                lanelets = lanelets.union(intersection_incoming.successors_left)
            if intersection_incoming.successors_right is not None:
                lanelets = lanelets.union(intersection_incoming.successors_right)
            if intersection_incoming.successors_straight is not None:
                lanelets = lanelets.union(intersection_incoming.successors_straight)

        return lanelets

    def get_intersection_by_lanelet_id(self, lanelet_id: int) -> Intersection | None:
        for intersection in self.scenario.lanelet_network.intersections:
            if lanelet_id in self.get_intersection_lanelet_ids(intersection):
                return intersection
        return None


class LaneletLayoutDivergingLane(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_DIVERGING_LANE

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        if (
            lanelet.successor is not None
            and len(lanelet.successor) > 1
            and not LaneletLayoutIntersection(self.scenario).is_fulfilled_for_lanelet(lanelet)
        ):
            return True
        return False


class LaneletLayoutMergingLane(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_MERGING_LANE

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        if (
            lanelet.predecessor is not None
            and len(lanelet.predecessor) > 1
            and not LaneletLayoutIntersection(self.scenario).is_fulfilled_for_lanelet(lanelet)
        ):
            return True
        return False


class LaneletLayoutRoundabout(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_LANELET_LAYOUT_ROUNDABOUT

    def is_fulfilled(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_fulfilled = self.is_fulfilled_for_lanelet(lanelet)
            if is_fulfilled:
                return True
        return False

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        if lanelet.successor is not None and lanelet.predecessor is not None:
            for successor_lanelet_id in lanelet.successor:
                if self.lanelet_in_roundabout(successor_lanelet_id, [lanelet.lanelet_id]):
                    return True
        return False

    def lanelet_in_roundabout(self, lanelet_id: int, encountered_lanelet_ids: list[int]):
        for lanelet in self.scenario.lanelet_network.lanelets:
            if lanelet.lanelet_id == lanelet_id:
                if (
                    lanelet.successor is not None
                    and len(set(encountered_lanelet_ids).intersection(lanelet.successor)) > 0
                ):
                    return True
                elif (
                    lanelet.successor is not None
                    and len(set(encountered_lanelet_ids).intersection(lanelet.successor)) == 0
                ):
                    for successor_lanelet_id in lanelet.successor:
                        if self.lanelet_in_roundabout(
                            successor_lanelet_id, [*encountered_lanelet_ids, successor_lanelet_id]
                        ):
                            return True
        return False
