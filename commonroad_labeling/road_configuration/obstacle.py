from commonroad.scenario.obstacle import ObstacleRole
from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.base import AutoLabelingBase
from commonroad_labeling.common.tag import Tag, TagGroup


class ObstacleLabeling(AutoLabelingBase):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag_group = TagGroup.OBSTACLE

    def scenario_contains_tag(self, tag: Tag) -> bool:
        if Tag(tag) == Tag.OBSTACLE_STATIC:
            return self.contains_static_obstacle()
        return False

    def contains_static_obstacle(self) -> bool:
        return any(obstacle.obstacle_role == ObstacleRole.STATIC for obstacle in self.scenario.obstacles)
