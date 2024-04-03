from pathlib import Path

from commonroad_labeling.criticality.cm_computer import compute_metrics

compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/ZAM_Over-1_1.xml")
