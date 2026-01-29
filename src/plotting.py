import matplotlib.pyplot as plt


def plot_enrichment_curve(df_curve, out_path):
    plt.figure(figsize=(6, 4))
    plt.plot(df_curve["percentile"], df_curve["yield_rate"], marker="o")
    plt.xlabel("Top percentile selected")
    plt.ylabel("Yield rate (event prevalence)")
    plt.title("Trial enrichment curve")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
