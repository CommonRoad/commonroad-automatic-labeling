from commonroad_route_planner.route import Route

from commonroad_labeling.common.tag import RouteTag, TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_obstacle import (
    ObstacleOtherDynamic,
    ObstacleStatic,
    ObstacleTraffic,
)


class RouteObstacleStatic(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleStatic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_STATIC


class RouteObstacleOtherDynamic(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleOtherDynamic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_OTHER_DYNAMIC


class RouteTrafficAhead(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleTraffic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_TRAFFIC_AHEAD


class RouteTrafficBehind(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleTraffic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_TRAFFIC_BEHIND

    def is_fulfilled(self) -> bool:
        lanelets = self.get_route_lanelets()

        for lanelet in lanelets:
            for predecessor_lanelet_id in lanelet.predecessor if lanelet.predecessor is not None else []:
                if self.scenario_tag.is_fulfilled_for_lanelet(
                    self.route.lanelet_network.find_lanelet_by_id(predecessor_lanelet_id)
                ):
                    return True

        return False


class RouteOncomingTraffic(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, ObstacleTraffic(route.scenario))
        self.tag = TagEnum.ROUTE_OBSTACLE_ONCOMING_TRAFFIC

    def is_fulfilled(self) -> bool:
        lanelets = self.get_route_lanelets()
        for lanelet in lanelets:
            if (
                lanelet.adj_left is not None
                and not lanelet.adj_left_same_direction
                and self.scenario_tag.is_fulfilled_for_lanelet(
                    self.route.lanelet_network.find_lanelet_by_id(lanelet.adj_left)
                )
            ) or (
                lanelet.adj_right is not None
                and not lanelet.adj_right_same_direction
                and self.scenario_tag.is_fulfilled_for_lanelet(
                    self.route.lanelet_network.find_lanelet_by_id(lanelet.adj_right)
                )
            ):
                return True

        self.tag = TagEnum.ROUTE_OBSTACLE_NO_ONCOMING_TRAFFIC
        return True
