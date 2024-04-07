# Computes criticality metrics for a scenario


from commonroad.common.file_reader import CommonRoadFileReader
from commonroad_crime.data_structure.configuration import CriMeConfiguration
from commonroad_crime.data_structure.crime_interface import CriMeInterface
from commonroad_crime.measure import HW, TTC, TTR, ALongReq, LongJ, BTN, P_MC, PF
import commonroad_crime.utility.visualization as utils_vis

from commonroad_labeling.criticality.trajectory_inserter import TrajectoryInserter


# If no ego_id is given, the vehicle will be generated from the planing problem using reactive planner
def compute_metrics(scenario_path: str, ego_id: str = None, save_plots=False, show_plots=False, make_gif=False,
                    do_log=False):
    scenario, planning_problem_set = CommonRoadFileReader(scenario_path).open()

    if ego_id is None:
        inserter = TrajectoryInserter(save_plots=save_plots, show_plots=show_plots, do_make_gif=make_gif, do_log=do_log)
        scenario, ego_id = inserter.insert_ego_trajectory(planning_problem_set, scenario)

    compute_metrics_for_id(scenario, ego_id)


# computes criticality metrics
def compute_metrics_for_id(scenario_with_ego, ego_id):
    config = create_crime_config(scenario_with_ego, ego_id)

    ts_start = 0
    ts_end = scenario_with_ego.obstacle_by_id(ego_id).prediction.trajectory.state_list[-1].time_step
    crime_interface = CriMeInterface(config)
    crime_interface.evaluate_scenario([HW, TTC, TTR, ALongReq, LongJ, BTN, P_MC, PF], ts_start, ts_end)
    # crime_interface.visualize(5)
    # utils_vis.plot_criticality_curve(crime_interface)


def create_crime_config(scenario_with_ego, ego_id):
    config = CriMeConfiguration()
    config.scenario = scenario_with_ego
    config.vehicle.ego_id = ego_id
    config.print_configuration_summary()
    config.debug.save_plots = False
    return config
