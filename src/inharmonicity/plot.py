import matplotlib.pyplot as plt
import numpy as np


def plot_frequencies(frequency_data: list[dict]):
    sorted_frequency_data = sorted(frequency_data, key=lambda k: k["string_gauge"])
    x_axis = [g_string["string_gauge"] for g_string in sorted_frequency_data]
    y_axis = [g_string["delta"] for g_string in sorted_frequency_data]

    table_labels = [
        "Gauge (mm)",
        "Fundamental (Hz)",
        "Ideal Harmonic (Hz)",
        "Measured Harmonic (Hz)",
        r"Delta ($\Delta f$)"
    ]
    table_data = [
        [
            f"{g_string['string_gauge']}",
            f"{g_string['fundamental']:.2f}",
            f"{g_string['ideal_harmonic']:.2f}",
            f"{g_string['measured_harmonic']:.2f}",
            f"{g_string['delta']:.2f}",
        ]
        for g_string in sorted_frequency_data
    ]

    figure_plot, axes_plot = plt.subplots()
    axes_plot.scatter(x_axis, y_axis)
    axes_plot.set_xlabel("String Gauge (mm)")
    axes_plot.set_ylabel(r"$\Delta f$ (Hz)")

    axes_plot.spines['top'].set_visible(False)
    axes_plot.spines['right'].set_visible(False)
    axes_plot.set_title("Inharmonicity Deviation on the 4th Harmonic")

    leastsq = np.polyfit(x_axis, y_axis, 2)

    poly_function = np.poly1d(leastsq)

    x_curve = np.linspace(x_axis[0], x_axis[-1], 100)

    ideal_y = poly_function(x_curve)

    axes_plot.plot(x_curve, ideal_y, color="black", linestyle="dashed")

    figure_plot.savefig("artifacts/inharmonicity_regression.pdf", format="pdf", dpi=300, bbox_inches="tight")

    figure_table, axes_table = plt.subplots()

    axes_table.axis("off")

    table = axes_table.table(
        cellText=table_data,
        colLabels=table_labels,
        loc="center",
        cellLoc="center",
        bbox=[0, 0, 1, 1],
    )

    table.auto_set_font_size(False)
    table.set_fontsize(5)
    table.scale(1, 1.5)

    figure_table.savefig("artifacts/inharmonicity_table.pdf", format="pdf", dpi=300, bbox_inches="tight")