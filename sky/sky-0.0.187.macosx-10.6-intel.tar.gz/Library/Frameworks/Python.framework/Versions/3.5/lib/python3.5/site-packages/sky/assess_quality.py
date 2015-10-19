def assess_news(doc):
    good_title = 3 < len(doc['title']) < 50
    good_body = 3 < len(' '.join(doc['body'])) < 50
    good_body = 20 < len(' '.join(doc['body'])) < 50

# def assess_news_per_source(doc):
