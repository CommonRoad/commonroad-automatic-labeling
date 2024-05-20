from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.scenario.state import InitialState
from commonroad.scenario.trajectory import Trajectory
from commonroad_rp.state import ReactivePlannerState


def find_egos_from_problem_sets(scenario_path: str):
    scenario, planning_problem_set = CommonRoadFileReader(scenario_path).open()
    return [
        problem.planning_problem_id - 90000
        for problem in planning_problem_set.planning_problem_dict.values()
    ]


def rp_state_to_init_state(rp_state: ReactivePlannerState):
    return InitialState(
        position=rp_state.position,
        orientation=rp_state.orientation,
        velocity=rp_state.velocity,
        acceleration=rp_state.acceleration,
        yaw_rate=rp_state.yaw_rate,
        time_step=rp_state.time_step,
    )


def compute_center_lanelet(ego_trajectory, scenario_with_ego):

    # Calculate lanelets of ego vehicle at all timesteps
    ego_center_lanelet_dict = dict(
        zip(
            [state.time_step for state in ego_trajectory],
            scenario_with_ego.lanelet_network.find_lanelet_by_position(
                [state.position for state in ego_trajectory]
            ),
        )
    )
    return ego_center_lanelet_dict
