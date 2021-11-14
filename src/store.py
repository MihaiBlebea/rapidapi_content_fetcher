from tinydb import TinyDB, Query, where

def store_scrape_results(results: list):
	db = TinyDB("./store/store.json")
	res = db.table("scrapes")
	res.insert(results[0])

def get_scrape_results(url: str) -> list:
	db = TinyDB("./store/store.json")
	scrapes = db.table("scrapes")
	res = scrapes.search(where("url") == url)
	if len(res) == 0:
		return None

	return res[0]

