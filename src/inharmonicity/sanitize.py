from pathlib import Path

import scipy.io as sio
from scipy.signal.windows import hann
import numpy as np

from system.paths import get_project_root

SAMPLE_RATE = 48000
BUFFER = 4800 # 100ms
WINDOW_SIZE = 4096

root_dir = get_project_root()
wav_directory = root_dir / "wav_files"
import_directory = wav_directory / "raw"
export_directory = wav_directory / "sanitized"

wav_list = []
t_0 = 0

for file in import_directory.iterdir():
    if file.suffix == ".wav":
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

        sio.wavfile.write(export_directory / f"{file.stem}_sanitized.wav", SAMPLE_RATE, windowed_signal.astype(np.float32))