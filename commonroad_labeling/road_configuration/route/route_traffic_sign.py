from commonroad_route_planner.route import Route

from commonroad_labeling.common.tag import RouteTag, TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_traffic_sign import (
    TrafficSignNoRightOfWay,
    TrafficSignRightOfWay,
    TrafficSignSpeedLimit,
    TrafficSignStopLine,
    TrafficSignTrafficLight,
)


class RouteTrafficSignSpeedLimit(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, TrafficSignSpeedLimit(route.scenario))
        self.tag = TagEnum.ROUTE_TRAFFIC_SIGN_SPEED_LIMIT


class RouteTrafficSignRightOfWay(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, TrafficSignRightOfWay(route.scenario))
        self.tag = TagEnum.ROUTE_TRAFFIC_SIGN_RIGHT_OF_WAY


class RouteTrafficSignNoRightOfWay(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, TrafficSignNoRightOfWay(route.scenario))
        self.tag = TagEnum.ROUTE_TRAFFIC_SIGN_NO_RIGHT_OF_WAY


class RouteTrafficSignStopLine(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, TrafficSignStopLine(route.scenario))
        self.tag = TagEnum.ROUTE_TRAFFIC_SIGN_STOP_LINE


class RouteTrafficSignTrafficLight(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, TrafficSignTrafficLight(route.scenario))
        self.tag = TagEnum.ROUTE_TRAFFIC_SIGN_TRAFFIC_LIGHT
