from pathlib import Path

from commonroad_labeling.criticality.cm_computer import CMComputer
from commonroad_crime.measure import *


metrics = [ALatReq, ALongReq, AReq, DST, HW, TTCE, WTTR, MSD, PSD, BTN, CI, CPI, STN, LatJ,
           LongJ, PF, P_MC, ET, PET, TET, THW, TIT, TTB, TTC, TTCStar, TTK, TTR, TTS, TTZ,
           WTTC, SOI, DCE, ]

cm_computer = CMComputer(metrics, verbose=True, overwrite=False)
scenario_dir = Path.cwd().joinpath("..", "scenarios", "MONA", "MONA-East")
cm_computer.compute_parallel(str(scenario_dir.absolute()), process_count=1)
