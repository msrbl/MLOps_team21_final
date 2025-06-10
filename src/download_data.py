import pathlib
import requests
import zipfile
import io

from config import DATA_DIR, DATASET_URL

def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DATA_DIR / "wine_quality.zip"

    if zip_path.exists():
        print("Archive already downloaded")
    else:
        print(f"Downloading {DATASET_URL} …")
        r = requests.get(DATASET_URL, timeout=60)
        r.raise_for_status()
        zip_path.write_bytes(r.content)
        print("Download complete")

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(DATA_DIR)
    print("Extraction done")

if __name__ == "__main__":
    main()