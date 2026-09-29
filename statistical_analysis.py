import numpy as np
import pandas as pd


def summarize_results(
    dataframe,
    metric_columns
):

    rows = []

    for policy in sorted(
        dataframe["policy"].unique()
    ):

        subset = dataframe[
            dataframe["policy"] == policy
        ]

        row = {
            "policy": policy
        }

        for metric in metric_columns:

            values = pd.to_numeric(
                subset[metric],
                errors="coerce"
            ).dropna()

            if len(values) == 0:

                row[f"{metric}_mean"] = np.nan
                row[f"{metric}_std"] = np.nan

            else:

                row[f"{metric}_mean"] = (
                    values.mean()
                )

                row[f"{metric}_std"] = (
                    values.std(
                        ddof=1
                    )
                    if len(values) > 1
                    else 0.0
                )

        rows.append(row)

    return pd.DataFrame(rows)