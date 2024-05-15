# Computes criticality metrics for a scenario
import logging
from multiprocessing import Pool

from commonroad.common.file_reader import CommonRoadFileReader
from commonroad_crime.data_structure.configuration import CriMeConfiguration
from commonroad_crime.data_structure.crime_interface import CriMeInterface
from commonroad_crime.measure import *
import commonroad_crime.utility.visualization as utils_vis
from pathlib import Path
from commonroad.scenario.scenario import Scenario

from commonroad_labeling.criticality.trajectory_inserter import TrajectoryInserter
from commonroad_labeling.criticality.crit_util import compute_center_lanelet, find_egos_from_problem_sets


class CMComputer:

    def __init__(self, verbose=False):
        self.verbose = verbose

    # If no ego_id is given, the vehicle will be generated from the planing problem using reactive planner
    def compute_metrics(self, scenario_path: str, ego_id: int = None, save_plots=False, show_plots=False, make_gif=False,
                        do_log=False):
        scenario, planning_problem_set = CommonRoadFileReader(scenario_path).open()

        if ego_id is None:
            inserter = TrajectoryInserter(save_plots=save_plots, show_plots=show_plots, do_make_gif=make_gif,
                                          do_log=do_log)
            scenario, ego_id = inserter.insert_ego_trajectory(planning_problem_set, scenario)

        self.compute_metrics_for_id(scenario, ego_id, scenario_path)

    # computes criticality metrics
    def compute_metrics_for_id(self, scenario_with_ego, ego_id, scenario_path, verbose=False):
        config = self.create_crime_config(scenario_with_ego, ego_id, scenario_path)

        ego_obstacle = scenario_with_ego.obstacle_by_id(ego_id)
        ts_start = ego_obstacle.initial_state.time_step
        ts_end = ego_obstacle.prediction.final_time_step

        all_states = ego_obstacle.prediction.trajectory.state_list
        all_states.insert(0, ego_obstacle.initial_state)

        if ego_obstacle.prediction.center_lanelet_assignment is None:
            ego_obstacle.prediction.center_lanelet_assignment = compute_center_lanelet(
                all_states, scenario_with_ego)

        crime_interface = CriMeInterface(config)
        # Errors in: DA, cant find route in route planner
        # Intended error?: TTM
        # SLOOOW: TCI

        # Out:ALatReq, ALongReq, AReq, DST, HW, TTCE, WTTR, MSD, PSD, BTN, CI, CPI,
        #     STN, LatJ, LongJ, PF, P_MC, ET, PET, TET, THW, TIT, TTB, TTC,
        #     TTCStar, TTK, TTR, TTS, TTZ, WTTC, SOI, DCE,

        metrics = [ALatReq, ALongReq, AReq, DST, HW, TTCE, WTTR, MSD, PSD, BTN, CI, CPI, STN, LatJ, LongJ, PF, P_MC, ET,
                   PET, TET, THW, TIT, TTB, TTC, TTCStar, TTK, TTR, TTS, TTZ, WTTC, SOI, DCE, ]

        if verbose:
            print(f"Started computing metrics for scenario {scenario_path}, ego_id {ego_id}")
        crime_interface.evaluate_scenario(
            metrics, ts_start,
            ts_end,
            verbose=self.verbose)

        # TODO: make output dir variable
        crime_interface.save_to_file(str(Path.cwd().joinpath("output")))

        # crime_interface.visualize(5)
        # utils_vis.plot_criticality_curve(crime_interface)

    def compute_parallel(self, scenario_dir: str):
        dir_path = Path(scenario_dir)
        all_scenarios = [str(x.absolute()) for x in list(dir_path.iterdir())]
        scenario_ego_pairs = []
        for scenario in all_scenarios:
            for ego_id in find_egos_from_problem_sets(scenario):
                scenario_ego_pairs.append([scenario, ego_id])
        with Pool() as pool:
            pool.imap_unordered(self.compute_metrics, scenario_ego_pairs)
            pool.close()
            pool.join()

    def create_crime_config(self, scenario_with_ego: Scenario, ego_id: int, scenario_path: str):
        config = CriMeConfiguration()
        config.general.name_scenario = str(scenario_with_ego.scenario_id)
        path_split = scenario_path.rsplit("/", 1)
        config.general.path_scenarios = path_split[0] + "/"
        config.scenario = scenario_with_ego
        config.vehicle.ego_id = ego_id
        config.debug.save_plots = False

        if self.verbose:
            config.print_configuration_summary()

        return config
