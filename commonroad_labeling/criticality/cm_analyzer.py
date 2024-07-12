import commonroad_crime
import pandas as pd
import inspect
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import MinMaxScaler

from commonroad_crime.measure import *
from commonroad_labeling.criticality.crime_output import ScenarioCriticalityData


# TODO Could be automatically checked like this, but not all CriMe metrics have individual monotonicity specified
#  (for example TTK, TTZ, WTTR) so manual review is safer until it is double checked that all metrics in CriMe have
#  correct monotonicity assigned
# for name, obj in inspect.getmembers(commonroad_crime.measure):
#     if inspect.isclass(obj) and issubclass(obj, CriMeBase) and obj.monotone == TypeMonotone.NEG:
#         print(name)
NEGATIVE_MONOTONE_METRICS = [ALongReq, DCE, HW, ET, PET, THW, TTC, TTCStar, TTCE, TTK, TTR, TTZ, WTTC, WTTR]

METADATA_COLUMN_NAMES = ["scenario_id", "ego_id", "timestep"]


def correlation_chooser(df, correlation_threshold: float, verbose=True):
    correlation_matrix = df.corr().abs()

    # Select upper triangle of correlation matrix
    upper = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))

    # Find features with correlation greater than correlation_threshold
    to_drop = []
    for column in upper.columns:
        correlated = upper[column] > correlation_threshold
        if any(correlated):
            if verbose:
                correlated_columns = correlated.index[correlated].tolist()
                print(
                    f"Dropping column '{column}' due to high correlation greater than {correlation_threshold} with columns: {correlated_columns}")
            to_drop.append(column)

    # Create a copy of the dataframe without the columns to be dropped
    df_selected = df.drop(columns=to_drop)

    return df_selected, to_drop


def robustness_chooser(original_df, threshold, verbose=True):
    df = original_df.copy()
    dropped_cols = []
    for col in df.columns:
        valid_count = df[col].replace([0, np.inf, -np.inf], np.nan).notna().sum()
        robustness = valid_count / len(df)
        if robustness < threshold:
            df.drop(col, axis=1, inplace=True)
            dropped_cols.append(col)
            if verbose:
                print(
                    f"Column '{col}' has been dropped since robustness of {robustness} is below threshold of {threshold}")
    return df, dropped_cols


def variance_chooser(df, variance_threshold: float, verbose=True):
    sel = VarianceThreshold(threshold=variance_threshold)
    sel.fit(df)
    selected_features_mask = sel.get_support()
    feature_names = df.columns

    # Get the names of the features that were removed
    removed_metrics = feature_names[~selected_features_mask]

    if verbose:
        print(
            f"The following metrics have been dropped since they did not meet the variance threshold of {variance_threshold}: " + " ".join(
                removed_metrics))

    # Create a new dataframe with only the selected features
    df_selected = df.loc[:, selected_features_mask]

    return df_selected, list(removed_metrics)


def invert_neg_mon_metrics(df):
    inverted_df = df.copy()
    contained_neg_scale_metric_names = [metric.measure_name for metric in NEGATIVE_MONOTONE_METRICS if
                                        metric.measure_name in inverted_df.columns]
    inverted_df.loc[:,
    [metric for metric in contained_neg_scale_metric_names]] = 1 - inverted_df.loc[:,
                                                                   [metric for metric in
                                                                    contained_neg_scale_metric_names]]
    return inverted_df


def choose_and_scale_metrics(df: pd.DataFrame, robustness_threshold: float, correlation_threshold: float,
                             variance_threshold: float, verbose=True):
    df_no_metadata = df.drop(METADATA_COLUMN_NAMES, axis=1)

    df_dropped, rob_dropped_metrics = robustness_chooser(df_no_metadata, threshold=robustness_threshold,
                                                         verbose=verbose)
    df_dropped = min_max_scale_df(df_dropped)
    df_dropped, var_dropped_metrics = variance_chooser(df_dropped, variance_threshold=variance_threshold,
                                                       verbose=verbose)
    df_dropped, cor_dropped_metrics = correlation_chooser(df_dropped, correlation_threshold, verbose=verbose)

    df_metadata = df[METADATA_COLUMN_NAMES]

    dropped_metrics = rob_dropped_metrics + var_dropped_metrics + cor_dropped_metrics
    accepted_metrics = df_no_metadata.columns.difference(dropped_metrics)
    return pd.concat([df_metadata, df_dropped], axis=1), accepted_metrics, dropped_metrics


def scale_metrics(df: pd.DataFrame):
    df_no_metadata = df.drop(METADATA_COLUMN_NAMES, axis=1)
    df_scaled = min_max_scale_df(df_no_metadata)

    df_metadata = df[METADATA_COLUMN_NAMES]
    return pd.concat([df_metadata, df_scaled], axis=1)


def calculate_row_average(df: pd.DataFrame) -> pd.DataFrame:
    average = df.drop(columns=["timestep"]).mean(axis=1)
    result_df = pd.DataFrame({'timestep': df['timestep'], 'average': average})
    return result_df


def find_max_average(df: pd.DataFrame) -> tuple:
    """
    Find the timestep in the given DataFrame `df` with the maximum average criticality and return it as a tuple.

    :param df: The DataFrame to search for the timestep with the maximum average criticality.
    :return: A tuple containing the timestep and average criticality value of the row with the maximum average.
    """
    max_average_index = df['average'].idxmax()
    max_average_row = df.loc[max_average_index]
    max_average_pair = (max_average_row['timestep'], max_average_row['average'])
    return max_average_pair


def get_scenario_average(df: pd.DataFrame, column_name: str) -> float:
    return df[column_name].mean()


def add_percentile_column(df, column_name):
    df[column_name + '_percentile'] = pd.qcut(df[column_name].rank(method='first'), q=100, labels=False) + 1
    return df


def filter_by_quantile(df, column_name, lower_quantile, upper_quantile):
    """
    Filters rows of a DataFrame based on whether the values in 'column_name' fall within the given quantile range.

    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    column_name (str): The name of the column to consider for the quantile range.
    lower_quantile (float): The lower quantile threshold (value between 0 and 1).
    upper_quantile (float): The upper quantile threshold (value between 0 and 1).

    Returns:
    pandas.DataFrame: A DataFrame with rows where 'column_name' is within the interquantile range.
    """
    lower_bound = df[column_name].quantile(lower_quantile)
    upper_bound = df[column_name].quantile(upper_quantile)

    return df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]


def analyze_criticality(crit_data_list: list[ScenarioCriticalityData], filter_metrics=True, robustness_threshold=0.1,
                        correlation_threshold=0.8, variance_threshold=0.01, verbose=True):
    df = crit_data_to_df(crit_data_list)

    if filter_metrics:
        scaled_df, accepted_metrics, dropped_metrics = choose_and_scale_metrics(df, robustness_threshold,
                                                                                correlation_threshold,
                                                                                variance_threshold, verbose=verbose)
    else:
        scaled_df = scale_metrics(df)
        accepted_metrics = None

    scaled_and_inverted_df = invert_neg_mon_metrics(scaled_df)
    grouped_by_scenario = scaled_and_inverted_df.groupby(["scenario_id", "ego_id"])
    scenario_data_df = {group_name: group_df.drop(["scenario_id", "ego_id"], axis=1) for group_name, group_df in
                        grouped_by_scenario}

    # Calculate average criticality value of each timestep
    scenario_timestep_averages = {keys: calculate_row_average(df) for keys, df in scenario_data_df.items()}

    # Find the timestep with the highest average criticality and safe its time and value
    most_dangerous_timesteps = {keys: find_max_average(df) for keys, df in scenario_timestep_averages.items()}
    # Calculate average crit over all timesteps of scenario and add column with percentiles
    scenario_averages = {keys: get_scenario_average(df, "average") for keys, df in scenario_timestep_averages.items()}
    scenario_average_list = [[scenario_id, ego_id, average_crit] for (scenario_id, ego_id), average_crit in
                             scenario_averages.items()]
    scenario_average_df = pd.DataFrame(scenario_average_list, columns=["scenario_id", "ego_id", "average_crit"])
    scenario_average_df["percentile"] = scenario_average_df["average_crit"].rank(pct=True)

    # Add column with percentiles for the data with each scenarios most dangerous timestep
    scenario_max_list = [[scenario_id, ego_id, timestep, average_crit] for
                         (scenario_id, ego_id), (timestep, average_crit) in most_dangerous_timesteps.items()]
    scenario_max_df = pd.DataFrame(scenario_max_list, columns=["scenario_id", "ego_id", "timestep", "average_crit"])
    scenario_max_df["percentile"] = scenario_max_df["average_crit"].rank(pct=True)

    return scenario_average_df, scenario_max_df, accepted_metrics


def crit_data_to_df(crit_data_list: list[ScenarioCriticalityData]) -> pd.DataFrame:
    criticality_dict_lists = []
    for scenario_data in crit_data_list:
        for timestep, crit_data in scenario_data.data.items():
            crit_data = copy.deepcopy(crit_data)

            crit_data["scenario_id"] = scenario_data.scenario_id
            crit_data["timestep"] = str(timestep)
            crit_data["ego_id"] = str(scenario_data.ego_id)
            criticality_dict_lists.append(crit_data)

    return pd.DataFrame(data=criticality_dict_lists)


def min_max_scale_df(df) -> pd.DataFrame:
    scaler = MinMaxScaler()
    normalized_df = df.copy()
    # Need to replace infinite values as they will become NaN after scaling otherwise
    for column in normalized_df.columns:
        # Check for positive infinity values and replace them with the non-infinite maximum of that column
        if (normalized_df[column] == np.inf).any():
            max_value = normalized_df[normalized_df[column] != np.inf][column].max()
            normalized_df[column] = normalized_df[column].replace(np.inf, max_value)

        # Check for negative infinity values and replace them with the non-infinite minimum of that colum
        if (normalized_df[column] == -np.inf).any():
            min_value = normalized_df[normalized_df[column] != -np.inf][column].min()
            normalized_df[column] = normalized_df[column].replace(-np.inf, min_value)
    normalized_df[normalized_df.columns] = scaler.fit_transform(normalized_df[normalized_df.columns])
    return normalized_df
