from scrapy import Spider
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from variables import get_variable


class ContentSpider(Spider):

	name = "content"

	start_url = None

	def __init__(self, url):
		self.start_url = url

	def start_requests(self):
		yield  SplashRequest(
			url=self.start_url, 
			callback=self.parse_content,
			args={
				"wait": 1
			},
			splash_url=get_variable("SPLASH_URL"),
			splash_headers={
				"Authorization": basic_auth_header(
					get_variable("SPLASH_USERNAME"), 
					get_variable("SPLASH_PASSWORD"),
				)
			},
			# meta={
			# 	"article_id": d["id"]
			# }
		)

	def parse_content(self, response):
		yield {
			"url": response.url,
			"title": response.css("title::text").get(),
			"description": self.__parse_meta_description(response),
			"content_text": self.__parse_content(response),
			"images": self.__parse_images(response),
			"links": self.__get_page_links(response),
			"tags": self.__parse_meta_tags(response),
			"keywords": self.__parse_meta_keywords(response)
		}

	def __get_page_links(self, response):
		base_url = self.__extract_host_from_url(response.url)
		links = []
		for link in response.css("a::attr(href)").getall():
			if link == "/" or link == "":
				continue
			links.append(self.__parse_link(base_url, link))
		return links

	def __extract_host_from_url(self, url: str) -> str:
		parsed_uri = urlparse(url)
		return "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)

	def __parse_content(self, response) -> list:
		soup = BeautifulSoup(response.body, "lxml")
		tags = soup.findAll(["h1", "h2", "h3", "h4", "h5", "h6", "p"])

		results = []
		for tag in tags:
			result = {}
			result[tag.name] = " ".join(tag.text.strip().split())
			results.append(result)
			
		return results

	def __parse_link(self, base_link, link: str) -> str:
		base_url = self.__extract_host_from_url(base_link)
		if "http" not in link:
			if link[0] == "/":
				link = base_url + link
			else:
				link = f"{base_url}/{link}"

		return link

	def __parse_images(self, response) -> list:
		base_url = self.__extract_host_from_url(response.url)
		soup = BeautifulSoup(response.body, "lxml")

		results = []
		for pic in soup.findAll("img"):
			link = pic.attrs.get("src", None)
			if link is None:
				continue
			results.append(self.__parse_link(base_url, link))

		return results

	def __parse_meta_description(self, response) -> str:
		desc = response.xpath("//meta[@name='description']/@content").get()
		if desc == "":
			desc = response.xpath("//meta[@name='og:description']/@content").get()
		
		return desc

	def __parse_meta_tags(self, response) -> list:
		result = []
		tags = response.xpath("//meta[@property='article:tag']/@content").get()
		if tags is None:
			return result

		tags = tags.split(",")
		for t in tags:
			result.append(t.strip())

		return result

	def __parse_meta_keywords(self, response) -> list:
		result = []
		tags = response.xpath("//meta[@name='keywords']/@content").get()
		if tags is None:
			return result

		return tags.split(" ")
