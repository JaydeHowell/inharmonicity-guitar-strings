import matplotlib.pyplot as plt
import numpy as np


def plot_frequencies(frequency_data: list[dict]):
    sorted_frequency_data = sorted(frequency_data, key=lambda k: k["string_gauge"])
    x_axis = [g_string["string_gauge"] for g_string in sorted_frequency_data]
    y_axis = [g_string["delta"] for g_string in sorted_frequency_data]

    figure, axes = plt.subplots()
    axes.scatter(x_axis, y_axis)
    axes.set_xlabel("String Gauge (mm)")
    axes.set_ylabel(r"$\Delta f$ (Hz)")

    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)

    leastsq = np.polyfit(x_axis, y_axis, 2)

    poly_function = np.poly1d(leastsq)

    x_curve = np.linspace(x_axis[0], x_axis[-1], 100)

    ideal_y = poly_function(x_curve)

    axes.plot(x_curve, ideal_y, color="black", linestyle="dashed")

    figure.savefig("inharmonicity_regression.pdf", format="pdf", dpi=300, bbox_inches="tight")