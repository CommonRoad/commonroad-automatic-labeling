from pathlib import Path

from commonroad_labeling.criticality.cm_computer import CMComputer


cm_computer = CMComputer(verbose=True)
scenario_dir = Path.cwd().joinpath("..", "scenarios", "inD_converted")
cm_computer.compute_parallel(str(scenario_dir.absolute()))

# compute_metrics(str(Path.cwd().joinpath("..", "scenarios", "MONA-2", "/C-DEU_MONAEast-2_1_T-199.xml")))