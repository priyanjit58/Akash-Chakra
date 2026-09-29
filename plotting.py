import os

import pandas as pd
import matplotlib.pyplot as plt


def plot_metric(
    dataframe,
    metric,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    policies = sorted(
        dataframe["policy"].unique()
    )

    values = []

    for policy in policies:

        subset = dataframe[
            dataframe["policy"] == policy
        ]

        values.append(
            pd.to_numeric(
                subset[metric],
                errors="coerce"
            ).dropna()
        )

    plt.figure(
        figsize=(9, 6)
    )

    plt.boxplot(
        values,
        labels=policies
    )

    plt.ylabel(metric)

    plt.title(
        f"{metric} comparison"
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200
    )

    plt.close()


def plot_policy_metric_means(
    dataframe,
    metric,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    grouped = (
        dataframe
        .groupby("policy")[metric]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    plt.figure(
        figsize=(9, 6)
    )

    grouped.plot(
        kind="bar"
    )

    plt.ylabel(metric)

    plt.title(
        f"Mean {metric} by policy"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200
    )

    plt.close()