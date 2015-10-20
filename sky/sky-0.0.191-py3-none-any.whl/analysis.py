from collections import Counter
import time


def avg_body(body):
    if not body:
        return 0
    return sum([len(x) for x in body]) / len(body)


def crawl_path_url_splitter(union):
    levels = {}
    for u in union:
        for level, x in enumerate(u.replace(':/', '').split('/')):
            if level not in levels:
                levels[level] = Counter()
            levels[level][x] += 1
    return levels


def crawl_path_analysis(good_union, bad_union, max_per_level=20):
    good_levels = crawl_path_url_splitter(good_union)
    bad_levels = crawl_path_url_splitter(bad_union)
    good_totals = {x: sum(good_levels[x].values()) for x in good_levels}
    # bad_totals = {x: sum(bad_levels[x].values()) for x in bad_levels}
    for level in bad_levels:
        for part in bad_levels[level]:
            times = bad_levels[level][part]
            if len(bad_levels[level]) > max_per_level:
                print("level {} too many parts ({}) in this level".format(
                    level, len(bad_levels[level])))
                break
            if level not in good_levels:
                print("level {} does not exist in good_levels: {}".format(level, part))
            elif part not in good_levels[level]:
                if bad_levels[level][part] > 1:
                    print("level {} bad part (not occuring in good): {} ({}/0)".format(level, part, times))
            elif bad_levels[level][part] > good_levels[level][part] * 3:
                tmp = "level {} bad part (occuring more in bad): {} ({}/{})"
                print(tmp.format(level, part, times, good_levels[level][part]))


def explore_crawl_path(docs, max_per_level=20):
    ddocs = [docs[x] for x in docs]
    per_source = {}
    today = time.strftime('%Y-%m-%d', time.gmtime())
    for domain in set([x['domain'] for x in ddocs]):
        print('------', domain, '------')
        sdocs = [x for x in ddocs if x['domain'] == domain]
        titles = set([x['url'] for x in sdocs if len(x['title']) < 4])
        bodys = set([x['url'] for x in sdocs if len(''.join(x['body'])) < 5 or
                     len(''.join(x['body'])) > 10000])
        dates = set([x['url'] for x in sdocs if len(x['publish_date']) != 10 or
                     x['publish_date'] == '1970-01-01' or x['publish_date'] > today])
        avg_bodys = set([x['url'] for x in sdocs if avg_body(x['body']) < 40])
        bad_union = dates.union(titles).union(bodys).union(avg_bodys)
        good_union = set([x['url'] for x in sdocs]) - bad_union
        crawl_path_analysis(good_union, bad_union, max_per_level)
        # c = Counter([sum([x in y for y in [titles, bodys, dates, avg_bodys]]) for x in bad_union])
        # print("bad results", c)


def document_is_okay(doc):
    today = time.strftime('%Y-%m-%d', time.gmtime())
    if len(doc['title']) < 4:
        return False
    if len(''.join(doc['body'])) < 5 or len(''.join(doc['body'])) > 10000:
        return False
    if (len(doc['publish_date']) != 10 or doc['publish_date'] == '1970-01-01' or
            doc['publish_date'] > today):
        return False
    if avg_body(doc['body']) < 40:
        return False
    return True
