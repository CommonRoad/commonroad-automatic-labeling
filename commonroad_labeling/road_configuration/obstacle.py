from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.obstacle import ObstacleRole
from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.tag import Tag, TagEnum


class ObstacleStatic(Tag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.OBSTACLE_STATIC

    def is_fulfilled(self) -> bool:
        return any(obstacle.obstacle_role == ObstacleRole.STATIC for obstacle in self.scenario.obstacles)

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        return len(lanelet.static_obstacles_on_lanelet) > 0
