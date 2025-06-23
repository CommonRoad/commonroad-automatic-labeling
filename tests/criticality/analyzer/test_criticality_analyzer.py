import numpy as np
import pandas as pd
import pytest

from commonroad_labeling.criticality.analyzer import cm_analyzer
from commonroad_labeling.criticality.analyzer.cm_analyzer import (
    NEGATIVE_MONOTONE_METRICS,
    min_max_scale_df,
    variance_chooser,
)


def test_min_max_scale_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        min_max_scale_df(df)


def test_min_max_scale_single_column():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
        }
    )
    result = min_max_scale_df(df)
    expected = pd.DataFrame(
        {
            "A": [0.0, 0.25, 0.5, 0.75, 1.0],
        },
        index=df.index,
    )
    pd.testing.assert_frame_equal(result, expected)


def test_min_max_scale_normal_values():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50],
        }
    )
    result = min_max_scale_df(df)
    expected = pd.DataFrame(
        {
            "A": [0.0, 0.25, 0.5, 0.75, 1.0],
            "B": [0.0, 0.25, 0.5, 0.75, 1.0],
        },
        index=df.index,
    )
    pd.testing.assert_frame_equal(result, expected)


def test_min_max_scale_with_infinite_values():
    df = pd.DataFrame(
        {
            "A": [1, 2, np.inf, 4, 5],
            "B": [10, -np.inf, 30, 40, 50],
        }
    )
    result = min_max_scale_df(df)
    expected = pd.DataFrame(
        {
            "A": [0.0, 0.25, 1.0, 0.75, 1.0],
            "B": [0.0, 0.0, 0.5, 0.75, 1.0],
        },
        index=df.index,
    )
    pd.testing.assert_frame_equal(result, expected)


def test_robustness_chooser():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [0, 2, np.inf, 4, 5],
            "C": [1, np.inf, 3, -np.inf, 5],
            "D": [1, 2, 3, 4, np.inf],
            "E": [np.inf, 2, 3, 4, 5],
        }
    )

    robust_df, dropped_cols = cm_analyzer.robustness_chooser(df, 0.8)

    assert robust_df.columns.tolist() == ["A", "D", "E"]
    assert dropped_cols == ["B", "C"]
    assert len(robust_df) == len(df)


def test_robustness_chooser_empty_dataframe():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        cm_analyzer.robustness_chooser(df, 0.8)


def test_robustness_chooser_invalid_threshold():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})

    with pytest.raises(ValueError):
        cm_analyzer.robustness_chooser(df, -0.1)

    with pytest.raises(ValueError):
        cm_analyzer.robustness_chooser(df, 1.1)


def test_correlation_chooser_without_correlated_columns():
    test_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [-10, 7, -8, -9, 20], "C": [0, 0, 0, 0, 0]})
    expected_df = test_df.copy()
    selected_df, dropped_columns = cm_analyzer.correlation_chooser(test_df, 0.9, False)
    pd.testing.assert_frame_equal(selected_df, expected_df)
    assert dropped_columns == []


def test_correlation_chooser_with_correlated_columns():
    test_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [1, 2, 3, 4, 5], "C": [11, 12, 13, 14, 15]})
    expected_df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
        }
    )
    selected_df, dropped_columns = cm_analyzer.correlation_chooser(test_df, 0.9, False)
    pd.testing.assert_frame_equal(selected_df, expected_df)
    assert dropped_columns == ["B", "C"]


def test_correlation_chooser_with_all_correlated_columns():
    test_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [1, 2, 3, 4, 5], "C": [1, 2, 3, 4, 5]})
    selected_df, dropped_columns = cm_analyzer.correlation_chooser(test_df, 0.9, False)
    expected_df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
    pd.testing.assert_frame_equal(selected_df, expected_df)
    assert dropped_columns == ["B", "C"]


def test_correlation_chooser_with_correlation_threshold_zero():
    test_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [1, 2, 3, 4, 5], "C": [11, 12, 13, 14, 15]})
    selected_df, dropped_columns = cm_analyzer.correlation_chooser(test_df, 0.0, False)
    assert selected_df.columns == ["A"]
    assert dropped_columns == ["B", "C"]


def test_correlation_chooser_with_empty_df():
    test_df = pd.DataFrame()
    with pytest.raises(ValueError):
        cm_analyzer.correlation_chooser(test_df, 0.9, False)


def test_variance_chooser_all_columns_removed():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1], "C": [2, 2, 2, 2, 2], "D": [3, 3, 3, 3, 3]})

    # sklearn throws ValueError when no feature meets the threshold.
    with pytest.raises(ValueError):
        variance_chooser(df, variance_threshold=5, verbose=False)


def test_variance_chooser_only_no_variance_removed():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1], "C": [2, 2, 2, 2, 2], "D": [3, 3, 3, 3, 3]})
    df_selected, removed_features = variance_chooser(df, variance_threshold=0, verbose=False)
    expected_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1]})
    pd.testing.assert_frame_equal(df_selected, expected_df)
    assert removed_features == ["C", "D"]


def test_variance_chooser_some_columns_removed():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1], "C": [2.1, 1.9, 1.9, 2.1, 2], "D": [3, 3, 3, 3, 3]})
    df_selected, removed_features = variance_chooser(df, variance_threshold=0.5, verbose=False)
    expected_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1]})
    pd.testing.assert_frame_equal(df_selected, expected_df)
    assert set(removed_features) == {"C", "D"}


def test_monotonicity_adjustment_all_neg_mono_metrics():
    df = pd.DataFrame({metric.measure_name: [0.1 + i * 0.1 for i in range(10)] for metric in NEGATIVE_MONOTONE_METRICS})
    adjusted_df = cm_analyzer.monotonicity_adjustment(df)
    # All metrics should be inverted
    for metric in NEGATIVE_MONOTONE_METRICS:
        assert (1 - df[metric.measure_name] == adjusted_df[metric.measure_name]).all()
    # The adjusted dataframe should have exactly one column for each metric
    assert len(adjusted_df.columns) == len(NEGATIVE_MONOTONE_METRICS)


def test_monotonicity_adjustment_partial_neg_mono_metrics():
    df = pd.DataFrame({metric.measure_name: [0.1 + i * 0.1 for i in range(10)] for metric in NEGATIVE_MONOTONE_METRICS})
    df["NonNegativeMetric"] = [0.4 + i * 0.1 for i in range(10)]
    adjusted_df = cm_analyzer.monotonicity_adjustment(df)
    for column in df.columns:
        if column in [metric.measure_name for metric in NEGATIVE_MONOTONE_METRICS]:
            assert (1 - df[column] == adjusted_df[column]).all()
        else:
            assert (df[column] == adjusted_df[column]).all()


def test_monotonicity_adjustment_no_neg_mono_metrics():
    df = pd.DataFrame({"NonNegativeMetric": [0.4 + i * 0.1 for i in range(10)]})
    adjusted_df = cm_analyzer.monotonicity_adjustment(df)
    assert df.equals(adjusted_df)  # The df should remain unchanged as there is no negative monotone metric.
