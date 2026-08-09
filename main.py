from inharmonicity.sanitize import sanitize
from inharmonicity.fft_i import get_fft
from inharmonicity.plot import plot_frequencies
from system.paths import get_project_root

from inharmonicity.constants import WINDOW_SIZE


def main():
    root_dir = get_project_root()
    wav_directory = root_dir / "wav_files"
    artifact_directory = root_dir / "artifacts"

    wav_directory.mkdir(exist_ok=True)

    processed_count, export_directory = sanitize(wav_directory)

    experiment_number = str(export_directory).split("\\")[-1]

    print(f"Processed {processed_count} files")

    frequency_data = get_fft(export_directory, WINDOW_SIZE)

    plot_frequencies(experiment_number, artifact_directory, frequency_data)

if __name__ == "__main__":
    main()

