import enum

from commonroad.scenario.lanelet import Lanelet
from commonroad.scenario.obstacle import DynamicObstacle, ObstacleRole, ObstacleType
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


class ObstacleTraffic(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_OBSTACLE_TRAFFIC

    def is_fulfilled(self) -> bool:
        return any(
            obstacle.obstacle_type in get_traffic_obstacle_types() for obstacle in self.scenario.dynamic_obstacles
        )

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        for obstacle_lanelet in get_dynamic_obstacles_lanelets_in_scenario(self.scenario, is_traffic=True):
            if obstacle_lanelet.lanelet_id == lanelet.lanelet_id:
                return True
        return False


class ObstacleOtherDynamic(ScenarioTag):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.tag = TagEnum.SCENARIO_OBSTACLE_OTHER_DYNAMIC

    def is_fulfilled(self) -> bool:
        return any(
            obstacle.obstacle_type not in get_traffic_obstacle_types() for obstacle in self.scenario.dynamic_obstacles
        )

    def is_fulfilled_for_lanelet(self, lanelet: Lanelet) -> bool:
        for obstacle_lanelet in get_dynamic_obstacles_lanelets_in_scenario(self.scenario, is_traffic=False):
            if obstacle_lanelet.lanelet_id == lanelet.lanelet_id:
                return True
        return False


def get_dynamic_obstacles_lanelets_in_scenario(scenario: Scenario, is_traffic: bool) -> set[Lanelet]:
    return set(
        [
            scenario.lanelet_network.find_lanelet_by_id(lanelet_id)
            for single_obstacle_lanelet_ids in [
                extract_lanelet_ids_for_single_obstacle(scenario, obstacle)
                for obstacle in extract_dynamic_obstacles_from_scenario(scenario, is_traffic)
            ]
            for lanelet_id in single_obstacle_lanelet_ids
        ]
    )


def extract_dynamic_obstacles_from_scenario(scenario: Scenario, is_traffic: bool) -> list[DynamicObstacle]:
    return list(
        filter(
            lambda obstacle: (is_traffic and obstacle.obstacle_type in get_traffic_obstacle_types())
            or (not is_traffic and obstacle.obstacle_type not in get_traffic_obstacle_types()),
            scenario.dynamic_obstacles,
        )
    )


def extract_lanelet_ids_for_single_obstacle(scenario: Scenario, obstacle: DynamicObstacle) -> set[int]:
    return set(
        [
            lanelet_id
            for lanelet_ids in scenario.lanelet_network.find_lanelet_by_position(
                [
                    obstacle.initial_state.position,
                    *(
                        [obstacle_state.position for obstacle_state in obstacle.prediction.trajectory.state_list]
                        if obstacle.prediction is not None
                        else []
                    ),
                ]
            )
            for lanelet_id in lanelet_ids
        ]
    )


def get_traffic_obstacle_types() -> list[enum]:
    return [
        ObstacleType.CAR,
        ObstacleType.TRUCK,
        ObstacleType.BUS,
        ObstacleType.BICYCLE,
        ObstacleType.PRIORITY_VEHICLE,
        ObstacleType.PARKED_VEHICLE,
        ObstacleType.TRAIN,
        ObstacleType.MOTORCYCLE,
        ObstacleType.TAXI,
    ]
