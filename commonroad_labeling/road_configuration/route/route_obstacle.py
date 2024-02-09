from commonroad_route_planner.route import Route

from commonroad_labeling.common.tag import RouteTag, TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_obstacle import ObstacleOtherDynamic, ObstacleStatic


class RouteObstacleStatic(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleStatic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_STATIC


class RouteObstacleOtherDynamic(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleOtherDynamic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_OTHER_DYNAMIC
