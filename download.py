import io
import zipfile
import requests

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_CSV = "ssa-baby-names.csv"

# Browser-like headers so the SSA server does not block the automated download
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


def main():
    # Download the zip archive into memory
    response = requests.get(URL, headers=HEADERS, timeout=60)
    response.raise_for_status()

    # Open the zip archive from the downloaded bytes
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        # Find all yearly files like "yob1880.txt" and sort them chronologically
        yob_files = sorted(
            name for name in zf.namelist()
            if name.startswith("yob") and name.endswith(".txt")
        )

        # Write all yearly data into a single CSV file with a header row
        with open(OUTPUT_CSV, "w", encoding="utf-8", newline="\n") as out_file:
            out_file.write("year,name,sex,count\n")

            for filename in yob_files:
                # Extract the 4-digit year from "yobYYYY.txt"
                year = filename[3:7]
                text = zf.read(filename).decode("utf-8")

                for line in text.splitlines():
                    if line:
                        out_file.write(f"{year},{line}\n")

    print(f"Created {OUTPUT_CSV} from {len(yob_files)} yearly files.")


if __name__ == "__main__":
    main()
