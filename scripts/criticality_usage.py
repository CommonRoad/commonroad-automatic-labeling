from pathlib import Path

from commonroad_labeling.criticality.cm_computer import compute_metrics

compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/ZAM_Over-1_1.xml")

# Fail with exception in CriMe:
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/BEL_Putte-8_2_T-1.xml")
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/DEU_Moelln-4_4_T-1.xml")
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/DEU_Moelln-10_2_T-1.xml")
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/ZAM_Tjunction-1_97_T-1.xml")

# Fail with AssertionError in Reactive Planner
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/DEU_Crit-1_1_T-1.xml")
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/DEU_Flensburg-10_1_T-1.xml")
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/DEU_Moabit-4_1_T-1.xml")
# compute_metrics(str(Path.cwd().joinpath("..", "scenarios")) + "/USA_US101-5_1_T-1.xml")

