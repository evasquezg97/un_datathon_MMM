import argparse
import sys
sys.path.append('.')
from src.scrapper import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    parser.add_argument("-o", "--output", type=str, default='result.csv')
    args = parser.parse_args()

    search_for = args.search if args.search else "Parks in Medellin"
    total = args.total if args.total else 1
    output_path = args.output

    main(output_path, search_for, total)