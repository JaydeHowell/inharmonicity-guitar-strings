from inharmonicity.sanitize import sanitize
from system.paths import get_project_root


def main():
    root_dir = get_project_root()
    wav_directory = root_dir / "wav_files"

    wav_directory.mkdir(exist_ok=True)

    processed_count = sanitize(wav_directory)

    print(f"Processed {processed_count} files")

if __name__ == "__main__":
    main()

