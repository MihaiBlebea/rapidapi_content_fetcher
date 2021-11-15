from tinydb import TinyDB, where

DB_TABLE = "scrapes"
DB_FILE = "./store/store.json"

def store_scrape_results(results: list):
	if len(results) == 0:
		return
		
	db = TinyDB(DB_FILE)
	res = db.table(DB_TABLE)
	res.insert(results[0])

def get_scrape_results(url: str) -> list:
	db = TinyDB(DB_FILE)
	scrapes = db.table(DB_TABLE)
	res = scrapes.search(where("url") == url)
	if len(res) == 0:
		return None

	return res[0]

