import argparse
import os

from store import DB_FILE
from scrape import scrape

def main():
	parser = argparse.ArgumentParser(
		prog= "scraper", 
		usage="%(prog)s [options] \"commands\"", 
		description="scrape content from url.",
	)

	parser.add_argument(
		"-cc",
		"--clear-cache",
		dest="clear_cache",
		required=False,
		action="store_true",
		help="rm the cache",
	)

	parser.add_argument(
		"-s",
		"--scrape",
		dest="scrape",
		required=False,
		action="store_true",
		help="scrape the link",
	)

	parser.add_argument(
		"-l",
		"--link",
		dest="link",
		required=False,
		help="link to scrape",
	)

	args = parser.parse_args()
	if args.clear_cache == True:
		if os.path.exists(DB_FILE):
			os.remove(DB_FILE)
		else:
			print(f"The file {DB_FILE} does not exist.")

	if args.scrape is True:
		if args.link is False:
			print("Please provide a link to scrape with -l command.")
		else:
			scrape(args.link)

if __name__ == "__main__":
	main()