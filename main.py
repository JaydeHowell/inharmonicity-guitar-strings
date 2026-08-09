from inharmonicity.sanitize import sanitize
from inharmonicity.fft_i import get_fft
from inharmonicity.plot import plot_frequencies
from system.paths import get_project_root

from inharmonicity.constants import WINDOW_SIZE


def main():
    root_dir = get_project_root()
    wav_directory = root_dir / "wav_files"

    wav_directory.mkdir(exist_ok=True)

    processed_count, export_directory = sanitize(wav_directory)

    print(f"Processed {processed_count} files")

    frequency_data = get_fft(export_directory, WINDOW_SIZE)

    plot_frequencies(frequency_data)

if __name__ == "__main__":
    main()

