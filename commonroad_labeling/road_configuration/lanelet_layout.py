from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.base import AutoLabelingBase
from commonroad_labeling.common.tag import Tag, TagGroup


class LaneletLayoutLabeling(AutoLabelingBase):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag_group = TagGroup.LANELET_LAYOUT

    def scenario_contains_tag(self, tag: Tag) -> bool:
        if Tag(tag) == Tag.LANELET_LAYOUT_SINGLE_LANE:
            return self.contains_single_lane()
        elif Tag(tag) == Tag.LANELET_LAYOUT_MULTI_LANE:
            return self.contains_multi_lane()
        elif Tag(tag) == Tag.LANELET_LAYOUT_BIDIRECTIONAL:
            return self.contains_bidirectional_roads()
        elif Tag(tag) == Tag.LANELET_LAYOUT_ONE_WAY:
            return self.contains_oneway_roads()
        elif Tag(tag) == Tag.LANELET_LAYOUT_INTERSECTION:
            return self.contains_intersection()
        return False

    def contains_single_lane(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            if (lanelet.adj_left_same_direction is None or not lanelet.adj_left_same_direction) \
                    and (lanelet.adj_right_same_direction is None and not lanelet.adj_right_same_direction):
                return True
        return False

    def contains_multi_lane(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            if (lanelet.adj_left_same_direction is not None and lanelet.adj_left_same_direction) \
                    or (lanelet.adj_right_same_direction is not None and lanelet.adj_right_same_direction):
                return True
        return False

    def contains_bidirectional_roads(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            if (lanelet.adj_left_same_direction is not None and not lanelet.adj_left_same_direction) \
                    or (lanelet.adj_right_same_direction is not None and not lanelet.adj_right_same_direction):
                return True
        return False

    def contains_oneway_roads(self) -> bool:
        for lanelet in self.scenario.lanelet_network.lanelets:
            is_one_way = True
            if lanelet.adj_left_same_direction is None or lanelet.adj_left_same_direction:
                is_one_way = is_one_way \
                             and self.adj_lanelet_has_same_dir_neighbors_or_none(lanelet.adj_left,
                                                                                 [lanelet.lanelet_id])
            else:
                is_one_way = False

            if lanelet.adj_right_same_direction is None or lanelet.adj_right_same_direction:
                is_one_way = is_one_way \
                             and self.adj_lanelet_has_same_dir_neighbors_or_none(lanelet.adj_right,
                                                                                 [lanelet.lanelet_id])
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
                if lanelet.adj_left_same_direction is None \
                        or (lanelet.adj_left not in previous_lanelet_ids and lanelet.adj_left_same_direction):
                    is_one_way = is_one_way \
                                 and self.adj_lanelet_has_same_dir_neighbors_or_none(lanelet.adj_left,
                                                                                     [*previous_lanelet_ids,
                                                                                      lanelet.lanelet_id])
                elif lanelet.adj_left not in previous_lanelet_ids:
                    is_one_way = False

                if lanelet.adj_right_same_direction is None \
                        or (lanelet.adj_right not in previous_lanelet_ids and lanelet.adj_right_same_direction):
                    is_one_way = is_one_way \
                                 and self.adj_lanelet_has_same_dir_neighbors_or_none(lanelet.adj_right,
                                                                                     [*previous_lanelet_ids,
                                                                                      lanelet.lanelet_id])
                elif lanelet.adj_right not in previous_lanelet_ids:
                    is_one_way = False

                return is_one_way

        return True

    def contains_intersection(self) -> bool:
        return len(self.scenario.lanelet_network.intersections) > 0
