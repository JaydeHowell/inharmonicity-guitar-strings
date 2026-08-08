from math import ceil
from pathlib import Path

import numpy as np
import scipy.io as sio
from scipy.fft import rfft

from inharmonicity.constants import (
    HERTZ_SEARCH_RANGE,
    BIN_WIDTH,
    FUNDAMENTAL_FREQUENCY,
    TARGET_HARMONIC,
)


def get_fft(wav_directory: Path, window_size) -> list[dict]:
    freq_table = []

    processing_directory = wav_directory / "sanitized"

    for file in processing_directory.iterdir():
        if file.suffix == ".wav":
            string_gauge_text = file.stem.split("_")[0]
            try:
                string_gauge = float(string_gauge_text) / 100
            except ValueError:
                raise ValueError(f"String gauge not found in {file.name}. Ensure file name starts with string gauge.")

            sample_rate, data = sio.wavfile.read(file)

            signal_array = rfft(data, n=window_size)

            magnitude_array = np.abs(signal_array)

            measured_fundamental = _get_fft_peak(FUNDAMENTAL_FREQUENCY, magnitude_array)
            ideal_harmonic = measured_fundamental * TARGET_HARMONIC
            measured_harmonic = _get_fft_peak(ideal_harmonic, magnitude_array)

            freq_delta = measured_harmonic - ideal_harmonic

            harmonic_data = {
                "file": file.name,
                "string_gauge": string_gauge,
                "fundamental": measured_fundamental,
                "ideal_harmonic": ideal_harmonic,
                "measured_harmonic": measured_harmonic,
                "delta": freq_delta,
            }

            freq_table.append(harmonic_data)

    return freq_table


def _get_fft_peak(frequency, magnitude_array) -> float:
    floor_value = 1e-10
    clipped_array = np.maximum(magnitude_array, floor_value)
    decibel_array = 20 * np.log10(clipped_array)

    fundamental_lower = int((frequency - HERTZ_SEARCH_RANGE) // BIN_WIDTH)
    fundamental_upper = int(ceil((frequency + HERTZ_SEARCH_RANGE) / BIN_WIDTH))

    freq_window = magnitude_array[fundamental_lower:fundamental_upper]
    local_index = np.argmax(freq_window)
    global_index = local_index + fundamental_lower

    fractional_offset = (((decibel_array[global_index - 1] - decibel_array[global_index + 1])
                         / (decibel_array[global_index - 1] - 2 * decibel_array[global_index]
                         + decibel_array[global_index + 1]))
                         / 2)

    freq_peak = (global_index + fractional_offset) * BIN_WIDTH

    return freq_peak