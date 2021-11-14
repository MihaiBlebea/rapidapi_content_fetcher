from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
import argparse

from spider import ContentSpider
from store import store_scrape_results

results = []

def crawler_results(signal, sender, item, response, spider):
	results.append(item)

def main():
	parser = argparse.ArgumentParser(
		prog= "scraper", 
		usage="%(prog)s [options] \"project\"", 
		description="scrape content from url.",
	)

	parser.add_argument(
		"-l",
		dest="link",
		required=True,
		help="link to scrape",
	)

	parser.add_argument(
		"-id",
		dest="scrape_id",
		required=True,
		help="scrape id to fetch back results",
	)

	args = parser.parse_args()
	
	dispatcher.connect(crawler_results, signal=signals.item_scraped)

	process = CrawlerProcess(settings={
		"SPLASH_URL": "http://127.0.0.1:8050",
		"DOWNLOADER_MIDDLEWARES": {
			"scrapy_splash.SplashCookiesMiddleware": 723,
			"scrapy_splash.SplashMiddleware": 725,
			"scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
		},
		"SPIDER_MIDDLEWARES": {
			"scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
		},
		"DUPEFILTER_CLASS": "scrapy_splash.SplashAwareDupeFilter",
		"HTTPCACHE_STORAGE": "scrapy_splash.SplashAwareFSCacheStorage"
	})

	process.crawl(ContentSpider, args.link)
	process.start()

	store_scrape_results(results)

	return results

if __name__ == "__main__":
	main()