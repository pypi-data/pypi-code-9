TITLE = ['//div[@class="document-title"]/div/text()',
         '//h1[@class="document-title"]/div/text()']
DESCRIPTION = ['//div[@class="id-app-orig-desc"]//text()']
CATEGORY = ['//span[@itemprop="genre"]/text()']


PRICE = ['//span[contains(@class, "is-price-tag")]/button/span[@class="display-price"]/text()']
DATE_PUBLISHED = ['//div[@itemprop="datePublished"]/text()']
OPERATING_SYSTEM = ['//div[@itemprop="operatingSystems"]/text()']
RATING_COUNT = ['//span[@class="reviews-num"]/text()']
RATING = ['//div[@class="score-container-star-rating"]/div/@aria-label']
CONTENT_RATING = ['//div[@itemprop="contentRating"]/text()']
CREATOR = ['//div[@itemprop="author"]/a/span[@itemprop="name"]/text()']
CREATOR_URL = ['//a[@class="document-subtitle primary"]/@href']
CREATOR_ADDRESS = ['//div[contains(@class, "content") and contains(@class, "physical-address")]/text()']
INSTALL_SIZE = ['//div[@itemprop="fileSize"]/text()']
DOWNLOAD_COUNT_TEXT = ['//div[@itemprop="numDownloads"]/text()']
PRIVACY_URL = ['//a[@class="dev-link" and contains(text(),"Privacy")]/@href']
WHATS_NEW = ['//div[@class="recent-change"]//text()']
