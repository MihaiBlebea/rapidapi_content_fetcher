from flask import Flask, jsonify, request, abort
import os
import time
import string

import store
from variables import get_variable

app = Flask(__name__)

@app.before_request
def before_request_func():
	proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

	if proxy_secret is None:
		return abort(401)

	if proxy_secret != get_variable("RAPIDAPI_PROXY_SECRET"):
		return abort(401)

@app.route("/scrape", methods=["GET"])
def scrape():
	url = request.args.get("url")
	if url is None:
		return jsonify({
			"error": True,
			"message": "no url query param"
		})

	result = get_or_scrape_content(url)

	return jsonify({
		"status": "OK",
		"url": url,
		"data": result
	})


@app.route("/chapters", methods=["GET"])
def chapters():
	url = request.args.get("url")
	min_freq = request.args.get("min_freq")
	
	if min_freq is None:
		min_freq = 0
	else:
		min_freq = int(min_freq)

	if url is None:
		return jsonify({
			"error": True,
			"message": "no url query param"
		})

	result = get_or_scrape_content(url)
	
	chapters = []
	for line in result["content_text"]:
		key = list(line.keys())[0]
		if "p" != key:
			chapters.append({
				"title": line[key],
				"content": "",
				"words": {}
			})
		else:
			chapters[-1]["content"] += f" {line[key]}"

	for chapter in chapters:
		content = chapter["content"].translate(str.maketrans("", "", string.punctuation))
		chapter["content"] = chapter["content"].strip()
		
		words = {}
		for word in content.split(" "):
			word = word.lower()
			if word in words:
				words[word] += 1
			else:
				words[word] = 1
		
		for word in words:
			if words[word] > min_freq:
				chapter["words"][word] = words[word]

	return jsonify({
		"status": "OK",
		"url": url,
		"data": chapters
	})

def get_or_scrape_content(url: str) -> dict:
	result = store.get_scrape_results(url)
	if result is None:
		os.system(f"./command.sh -s -l={url}")

		attempts = 3
		for i in range(attempts):
			result = store.get_scrape_results(url)
			if result is None:
				time.sleep(0.5)
			else:
				break

	return result

if __name__ == "__main__":
	app.run(debug=False)