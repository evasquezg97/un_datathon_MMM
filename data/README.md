# Maps Info scrapper

This is a simple python script that scrapes the maps information from the google maps website and simple google to get the information of the maps up to a search query.

## Installation

Clone this repo, install the requirements and run the script.

```bash
git clone ...
cd maps-info-scrapper
pip install -r requirements.txt
python maps_info_scrapper.py
```

## Usage

For a single search run the main script and enter the search query.

```bash
python scripts/single_search.py -s "gelato Medellin" -t 25 -o "output.csv"
```

This will search for the query "gelato Medellin" and get the information of the first 25 results, it will put the information in the file "output.csv".

For the information of multiple searches run the main script and enter the search queries in a file.

```bash
python scripts/multiple_search.py -f "searches.txt" -t 25 -o "output.csv"
```