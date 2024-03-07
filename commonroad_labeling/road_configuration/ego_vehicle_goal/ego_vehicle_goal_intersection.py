from commonroad_route_planner.route import Route

from commonroad_labeling.common.tag import EgoVehicleGoal, TagEnum
from commonroad_labeling.road_configuration.scenario.scenario_lanelet_layout import LaneletLayoutIntersection


class EgoVehicleGoalIntersectionTurnLeft(EgoVehicleGoal):
    def __init__(self, route: Route):
        super().__init__(route)
        self.tag = TagEnum.EGO_VEHICLE_GOAL_INTERSECTION_TURN_LEFT

    def is_fulfilled(self) -> bool:
        lanelets = self.get_route_lanelets()
        for lanelet in lanelets:
            intersection = LaneletLayoutIntersection(self.route.scenario).get_intersection_by_lanelet_id(
                lanelet.lanelet_id
            )

            if intersection is not None:
                for incoming in intersection.incomings:
                    if lanelet.lanelet_id in incoming.successors_left:
                        return True

        return False


class EgoVehicleGoalIntersectionTurnRight(EgoVehicleGoal):
    def __init__(self, route: Route):
        super().__init__(route)
        self.tag = TagEnum.EGO_VEHICLE_GOAL_INTERSECTION_TURN_RIGHT

    def is_fulfilled(self) -> bool:
        lanelets = self.get_route_lanelets()
        for lanelet in lanelets:
            intersection = LaneletLayoutIntersection(self.route.scenario).get_intersection_by_lanelet_id(
                lanelet.lanelet_id
            )

            if intersection is not None:
                for incoming in intersection.incomings:
                    if lanelet.lanelet_id in incoming.successors_right:
                        return True

        return False


class EgoVehicleGoalIntersectionProceedStraight(EgoVehicleGoal):
    def __init__(self, route: Route):
        super().__init__(route)
        self.tag = TagEnum.EGO_VEHICLE_GOAL_INTERSECTION_PROCEED_STRAIGHT

    def is_fulfilled(self) -> bool:
        lanelets = self.get_route_lanelets()
        for lanelet in lanelets:
            intersection = LaneletLayoutIntersection(self.route.scenario).get_intersection_by_lanelet_id(
                lanelet.lanelet_id
            )

            if intersection is not None:
                for incoming in intersection.incomings:
                    if lanelet.lanelet_id in incoming.successors_straight:
                        return True

        return False
