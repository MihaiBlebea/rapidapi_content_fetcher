from flask import Flask, jsonify, request, abort
import os
import time
from dotenv import dotenv_values

from store import get_scrape_results

app = Flask(__name__)

config = dotenv_values(".env")

def get_proxy_secret_env() -> str:
	config = dotenv_values(".env")
	if "RAPIDAPI_PROXY_SECRET" not in config:
		return os.getenv("RAPIDAPI_PROXY_SECRET")

	return config["RAPIDAPI_PROXY_SECRET"]


@app.route("/scrape", methods=["GET"])
def scrape():
	proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")
	
	if proxy_secret is None:
		return abort(401)

	if proxy_secret != get_proxy_secret_env():
		return abort(401)

	url = request.args.get("url")
	if url is None:
		return jsonify({
			"error": True,
			"message": "no url query param"
		})

	result = get_scrape_results(url)
	if result is None:
		os.system(f"./virtualenv/bin/python3 ./src/scrape.py -l={url} -id=1")

		attempts = 3
		for i in range(attempts):
			result = get_scrape_results(url)
			if result is None:
				time.sleep(0.5)
			else:
				break

	return jsonify({
		"status": "OK",
		"url": url,
		"data": result
	})

if __name__ == "__main__":
	app.run(debug=False)