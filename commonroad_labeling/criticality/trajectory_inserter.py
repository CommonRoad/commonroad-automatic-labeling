# Calculates a trajectory for the ego vehicle using CommonRoad Reactive Planner and inserts it into the scenario
import logging
from copy import deepcopy

from commonroad.geometry.shape import Rectangle
from commonroad.planning.planning_problem import PlanningProblemSet
from commonroad.prediction.prediction import TrajectoryPrediction
from commonroad.scenario.obstacle import DynamicObstacle, ObstacleType
from commonroad.scenario.scenario import Scenario
from commonroad.scenario.state import InitialState
from commonroad.scenario.trajectory import Trajectory
from commonroad_route_planner.route_planner import RoutePlanner
from commonroad_rp.reactive_planner import ReactivePlanner
from commonroad_rp.state import ReactivePlannerState
from commonroad_rp.utility.config import ReactivePlannerConfiguration
from commonroad_rp.utility.logger import initialize_logger
from commonroad_rp.utility.visualization import make_gif, visualize_planner_at_timestep


class TrajectoryInserter:

    def __init__(
        self, save_plots=False, show_plots=False, do_make_gif=False, do_log=False
    ):
        self.save_plots: bool = save_plots
        self.show_plots: bool = show_plots
        self.make_gif: bool = do_make_gif
        self.do_log: bool = do_log

    def insert_ego_trajectory(self, planning_problem_set, scenario):
        scenario_with_ego = deepcopy(scenario)

        # Calculate trajectory of ego vehicle
        ego_rp_trajectory, ego_vehicle_params = self.get_default_trajectory(
            scenario_with_ego, planning_problem_set
        )

        # Create properties of ego vehicle needed to create it as a dynamic obstacle
        ego_shape = Rectangle(
            width=ego_vehicle_params.width, length=ego_vehicle_params.length
        )
        ego_id = scenario_with_ego.generate_object_id()
        ego_initial_state = self.rp_state_to_init_state(ego_rp_trajectory[0])
        ego_trajectory = Trajectory(1, ego_rp_trajectory[1:])

        # Calculate lanelets of ego vehicle at all timesteps
        ego_center_lanelet_dict = dict(
            zip(
                [state.time_step for state in ego_rp_trajectory],
                scenario_with_ego.lanelet_network.find_lanelet_by_position(
                    [state.position for state in ego_rp_trajectory]
                ),
            )
        )
        ego_prediction = TrajectoryPrediction(
            ego_trajectory, ego_shape, center_lanelet_assignment=ego_center_lanelet_dict
        )
        # Create dynamic obstacle

        ego_obstacle = DynamicObstacle(
            ego_id,
            ObstacleType.CAR,
            ego_shape,
            initial_state=ego_initial_state,
            prediction=ego_prediction,
        )

        # Insert ego vehicle into scenario as dynamic obstacle
        scenario_with_ego.add_objects(ego_obstacle)
        return scenario_with_ego, ego_id

    # calculates trajectory of ego vehicle with commonroad reactive planner
    def get_default_trajectory(
        self, scenario: Scenario, planing_problem_set: PlanningProblemSet
    ):
        config = self.create_config(planing_problem_set, scenario)

        # Mostly copied from reactive_planner tutorial:

        # initialize and get logger
        if self.do_log:
            initialize_logger(config)
            logger = logging.getLogger("RP_LOGGER")

        # *************************************
        # Initialize Planner
        # *************************************
        # run route planner and add reference path to config
        route_planner = RoutePlanner(config.scenario, config.planning_problem)
        route = route_planner.plan_routes().retrieve_first_route()
        config.planning.route = route
        config.planning.reference_path = route.reference_path

        # initialize reactive planner
        planner = ReactivePlanner(config)

        # **************************
        # Run Planning
        # **************************
        # Add first state to recorded state and input list
        planner.record_state_and_input(planner.x_0)

        SAMPLING_ITERATION_IN_PLANNER = True

        while not planner.goal_reached():
            current_count = len(planner.record_state_list) - 1

            # check if planning cycle or not
            plan_new_trajectory = (
                current_count % config.planning.replanning_frequency == 0
            )
            if plan_new_trajectory:
                # new planning cycle -> plan a new optimal trajectory
                planner.set_desired_velocity(current_speed=planner.x_0.velocity)
                if SAMPLING_ITERATION_IN_PLANNER:
                    optimal = planner.plan()
                else:
                    optimal = None
                    i = 1
                    while optimal is None and i <= planner.sampling_level:
                        optimal = planner.plan(i)

                if not optimal:
                    break

                # record state and input
                planner.record_state_and_input(optimal[0].state_list[1])

                # reset planner state for re-planning
                planner.reset(
                    initial_state_cart=planner.record_state_list[-1],
                    initial_state_curv=(optimal[2][1], optimal[3][1]),
                    collision_checker=planner.collision_checker,
                    coordinate_system=planner.coordinate_system,
                )

                # visualization: create ego Vehicle for planned trajectory and store sampled trajectory set
                if config.debug.show_plots or config.debug.save_plots:
                    ego_vehicle = planner.convert_state_list_to_commonroad_object(
                        optimal[0].state_list
                    )
                    sampled_trajectory_bundle = None
                    if config.debug.draw_traj_set:
                        sampled_trajectory_bundle = deepcopy(
                            planner.stored_trajectories
                        )
            else:
                # simulate scenario one step forward with planned trajectory
                sampled_trajectory_bundle = None

                # continue on optimal trajectory
                temp = current_count % config.planning.replanning_frequency

                # record state and input
                planner.record_state_and_input(optimal[0].state_list[1 + temp])

                # reset planner state for re-planning
                planner.reset(
                    initial_state_cart=planner.record_state_list[-1],
                    initial_state_curv=(optimal[2][1 + temp], optimal[3][1 + temp]),
                    collision_checker=planner.collision_checker,
                    coordinate_system=planner.coordinate_system,
                )

            print(f"current time step: {current_count}")

            # visualize the current time step of the simulation
            if config.debug.show_plots or config.debug.save_plots:
                visualize_planner_at_timestep(
                    scenario=config.scenario,
                    planning_problem=config.planning_problem,
                    ego=ego_vehicle,
                    traj_set=sampled_trajectory_bundle,
                    ref_path=planner.reference_path,
                    timestep=current_count,
                    config=config,
                )

        # make gif
        if self.make_gif:
            make_gif(config, range(0, planner.record_state_list[-1].time_step))

        return planner.record_state_list, planner.vehicle_params

    def create_config(self, planing_problem_set, scenario):
        # Get planing_problem from planing_problem_set
        planning_problem = self.get_planing_problem(planing_problem_set)

        config = ReactivePlannerConfiguration()

        config.scenario = scenario

        config.planning_problem_set = planing_problem_set
        config.planning_problem = planning_problem
        config.planning.dt = 0.1
        config.planning.replanning_frequency = 3
        config.planning.time_steps_computation = 20

        config.vehicle.id_type_vehicle = 2

        config.debug.draw_icons = True
        config.debug.num_workers = 10

        config.debug.save_plots = self.save_plots
        config.debug.show_plots = self.show_plots

        return config

    def get_planing_problem(self, planing_problem_set):
        planning_problem_dict = planing_problem_set.planning_problem_dict
        if len(planning_problem_dict) == 1:
            planning_problem = list(planning_problem_dict.values()).pop()
        else:
            RuntimeError("Not exactly one planning_problem in planning_problem_set")
            return
        return planning_problem

    def rp_state_to_init_state(self, rp_state: ReactivePlannerState):
        return InitialState(
            position=rp_state.position,
            orientation=rp_state.orientation,
            velocity=rp_state.velocity,
            acceleration=rp_state.acceleration,
            yaw_rate=rp_state.yaw_rate,
            time_step=rp_state.time_step,
        )
