from flask import Flask, jsonify, request, abort
import os
import time

from store import get_scrape_results

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
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