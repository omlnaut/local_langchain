from urllib.parse import urljoin

import scrapy


class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"

    def start_requests(self):
        asin_list = ["B09G9FPHY6"]
        for asin in asin_list:
            amazon_reviews_url = f"https://www.amazon.com/product-reviews/{asin}/"
            yield scrapy.Request(
                url=amazon_reviews_url, callback=self.parse_reviews, meta={"asin": asin}
            )

    def parse_reviews(self, response):
        asin = response.meta["asin"]

        ## Parse Product Reviews
        review_elements = response.css("#cm_cr-review_list div.review")
        for review_element in review_elements:
            yield {
                "asin": asin,
                "text": "".join(
                    review_element.css("span[data-hook=review-body] ::text").getall()
                ).strip(),
                "title": review_element.css(
                    "*[data-hook=review-title]>span::text"
                ).get(),
                "location_and_date": review_element.css(
                    "span[data-hook=review-date] ::text"
                ).get(),
                "verified": bool(
                    review_element.css("span[data-hook=avp-badge] ::text").get()
                ),
                "rating": review_element.css(
                    "*[data-hook*=review-star-rating] ::text"
                ).re(r"(\d+\.*\d*) out")[0],
            }
