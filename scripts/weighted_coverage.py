import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

def load_merged_data(path):
    df = pd.read_csv(path)
    print(f"✅ Loaded merged data: {df.shape[0]} rows")
    return df


def classify_track_status(df):
    df['track_group'] = df['track_status'].map({
        'Achieved': 'on-track',
        'On Track': 'on-track',
        'Acceleration Needed': 'off-track'
    })
    return df


def compute_weighted_averages(df):
    grouped = df.groupby('track_group')
    results = grouped.apply(lambda g: pd.Series({
        'ANC4_weighted': (g['anc4_coverage'] * g['births_2022']).sum() / g['births_2022'].sum(),
        'SBA_weighted': (g['sba_coverage'] * g['births_2022']).sum() / g['births_2022'].sum()
    }))
    results = results.reset_index()
    return results


def plot_comparison(results, output_path):
    # Transform for plotting
    melted = results.melt(id_vars='track_group', var_name='Indicator', value_name='Coverage')
    melted['Indicator'] = melted['Indicator'].str.replace('_weighted', '')

    plt.figure(figsize=(7, 5))
    sns.set_style("whitegrid")

    ax = sns.barplot(
        data=melted,
        x='Indicator',
        y='Coverage',
        hue='track_group',
        palette={'on-track': '#2ca02c', 'off-track': '#d62728'}
    )

    # Add coverage labels inside bars
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", label_type='center', color='white', fontsize=10)

    plt.title("📊 Population-Weighted Coverage of ANC4 & SBA")
    plt.ylabel("Coverage (%)")
    plt.xlabel("Indicator")
    plt.legend(title="Track Group", loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"📊 Saved improved plot to {output_path}")


def main():
    ROOT = Path(__file__).resolve().parents[2]
    merged_path = ROOT / "data" / "interim" / "coverage_2022_merged.csv"
    output_csv = ROOT / "data" / "processed" / "weighted_results.csv"
    output_plot = ROOT / "outputs" / "weighted_plot.png"
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    df = load_merged_data(merged_path)
    df = classify_track_status(df)
    results = compute_weighted_averages(df)

    results.to_csv(output_csv, index=False)
    print(f"📄 Saved weighted results to {output_csv}")

    plot_comparison(results, output_plot)


if __name__ == '__main__':
    main()
