import enum

from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.obstacle import ObstacleRole, ObstacleType
from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.tag import ScenarioTag, TagEnum


class ObstacleStatic(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_OBSTACLE_STATIC

    def is_fulfilled(self) -> bool:
        return any(obstacle.obstacle_role == ObstacleRole.STATIC for obstacle in self.scenario.obstacles)

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        return len(lanelet.static_obstacles_on_lanelet) > 0


class ObstacleOtherDynamic(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_OBSTACLE_OTHER_DYNAMIC

    def is_fulfilled(self) -> bool:
        return any(
            (obstacle.obstacle_role == ObstacleRole.DYNAMIC and obstacle.obstacle_type in self.get_obstacle_types())
            for obstacle in self.scenario.obstacles
        )

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        return len(lanelet.dynamic_obstacles_on_lanelet) > 0

    def get_obstacle_types(self) -> list[enum]:
        return [
            ObstacleType.UNKNOWN,
            ObstacleType.PEDESTRIAN,
            ObstacleType.CONSTRUCTION_ZONE,
            ObstacleType.ROAD_BOUNDARY,
            ObstacleType.BUILDING,
            ObstacleType.PILLAR,
            ObstacleType.MEDIAN_STRIP,
        ]
