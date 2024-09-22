from pathlib import Path

import pytest
from commonroad_crime.data_structure.base import CriMeBase
from commonroad_crime.measure import (
    BTN,
    CI,
    CPI,
    DCE,
    DST,
    ET,
    HW,
    MSD,
    P_MC,
    PET,
    PF,
    PSD,
    SOI,
    STN,
    TET,
    THW,
    TIT,
    TTB,
    TTC,
    TTCE,
    TTK,
    TTR,
    TTS,
    TTZ,
    WTTC,
    WTTR,
    ALatReq,
    ALongReq,
    AReq,
    LatJ,
    LongJ,
    TTCStar,
)

from commonroad_labeling.criticality.computer.cm_computer import CMComputer
from commonroad_labeling.criticality.computer.crit_util import find_egos_from_problem_sets

metrics = [
    ALatReq,
    ALongReq,
    AReq,
    DST,
    HW,
    TTCE,
    WTTR,
    MSD,
    PSD,
    BTN,
    CI,
    CPI,
    STN,
    LatJ,
    LongJ,
    PF,
    P_MC,
    ET,
    PET,
    TET,
    THW,
    TIT,
    TTB,
    TTC,
    TTCStar,
    TTK,
    TTR,
    TTS,
    TTZ,
    WTTC,
    SOI,
    DCE,
]


# TODO: Only testing for one scenario currently! Should be increased if performance allows it.
@pytest.mark.parametrize("scenario_path", list(Path.cwd().joinpath("test_scenarios").iterdir())[:1])
@pytest.mark.parametrize("metric", metrics)
def test_metric_computation_test_base(metric: CriMeBase, scenario_path: Path):
    scenario_string = str(scenario_path.absolute())
    test_output_dir = Path.cwd().joinpath("test_output")
    if not test_output_dir.exists():
        test_output_dir.mkdir()
    # clear directory containing test output
    for path in test_output_dir.iterdir():
        if path.is_file():
            path.unlink()
    # compute the metric for ego vehicles in the scenario
    ego_ids = find_egos_from_problem_sets(scenario_string)
    cm_computer = CMComputer(metrics=[metric], overwrite=False, verbose=True, crime_verbose=False)
    for ego_id in ego_ids:
        cm_computer.compute_metrics(
            scenario_path=scenario_string, ego_id=ego_id, output_dir=str(test_output_dir.absolute())
        )
    # make sure the output files exists
    for ego_id in ego_ids:
        assert Path(test_output_dir).joinpath(f"CriMe-{scenario_path.name[:-4]}_veh_{ego_id}.xml").exists()
