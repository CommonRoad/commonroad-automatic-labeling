from commonroad_route_planner.route import Route

from commonroad_labeling.common.tag import RouteTag, TagEnum
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


class RouteLaneletLayoutSingleLane(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutSingleLane(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_SINGLE_LANE


class RouteLaneletLayoutMultiLane(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutMultiLane(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_MULTI_LANE


class RouteLaneletLayoutBidirectional(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutBidirectional(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_BIDIRECTIONAL


class RouteLaneletLayoutOneWay(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutOneWay(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_ONE_WAY


class RouteLaneletLayoutIntersection(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutIntersection(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_INTERSECTION


class RouteLaneletLayoutDivergingLane(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutDivergingLane(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_DIVERGING_LANE


class RouteLaneletLayoutMergingLane(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutMergingLane(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_MERGING_LANE


class RouteLaneletLayoutRoundabout(RouteTag):
    def __init__(self, route: Route):
        super().__init__(route, LaneletLayoutRoundabout(route.scenario))
        self.tag = TagEnum.ROUTE_LANELET_LAYOUT_ROUNDABOUT
