from pathlib import Path

import numpy as np
import scipy.io as sio
from scipy.signal.windows import hann

from inharmonicity.constants import (
    SAMPLE_RATE,
    BUFFER,
    WINDOW_SIZE,
)
from system.paths import get_folder_iteration


def sanitize(wav_directory: Path) -> (int, Path):
    import_directory = wav_directory / "raw"
    export_parent_directory = wav_directory / "sanitized"

    iteration = str(get_folder_iteration(export_parent_directory))

    export_directory = export_parent_directory / f"experiment_{iteration.zfill(3)}"
    export_directory.mkdir(parents=True, exist_ok=True)

    count = 0

    for file in import_directory.iterdir():
        if file.suffix == ".wav":
            string_gauge_text = file.stem.split("_")[0]
            try:
                string_gauge = float(string_gauge_text) / 100
            except ValueError:
                print(
                    f"Warning: String gauge not found in {file.name}. Ensure file names start with string gauge. Skipping...")
                continue

            sample_rate, data = sio.wavfile.read(file)
            if sample_rate != SAMPLE_RATE:
                raise ValueError(f"sample rate {sample_rate} does not equal the expected {SAMPLE_RATE}")

            print(f"Processed {file.name} at sample rate {sample_rate}")

            if data.ndim != 1:
                raise ValueError(f"Expected 1D array, got {data.ndim} instead")

            t_0 = np.argmax(np.abs(data))
            start_i = t_0 + BUFFER

            if start_i + WINDOW_SIZE > len(data):
                raise ValueError(f"{file.name} does not contain enough samples beyond peak amplitude.")

            data_slice = data[start_i:start_i + WINDOW_SIZE]

            window = hann(WINDOW_SIZE, sym=False)
            windowed_signal = data_slice * window

            sio.wavfile.write(export_directory / f"{file.stem}_sanitized.wav", SAMPLE_RATE,
                              windowed_signal.astype(np.float32))
            count += 1

    return count, export_directory