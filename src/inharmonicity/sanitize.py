from pathlib import Path

import numpy as np
import scipy.io as sio
from scipy.signal.windows import hann

from inharmonicity.constants import (
    SAMPLE_RATE,
    BUFFER,
    WINDOW_SIZE,
)


def sanitize(wav_directory: Path) -> int:
    import_directory = wav_directory / "raw"
    export_directory = wav_directory / "sanitized"

    count = 0

    for file in import_directory.iterdir():
        if file.suffix == ".wav":
            try:
                string_gauge = float(file.stem.split("_")[0])
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

    return count