from pathlib import Path

from commonroad_labeling.common.general import go_through_dir

go_through_dir(Path.cwd().joinpath("..", "scenarios"))
