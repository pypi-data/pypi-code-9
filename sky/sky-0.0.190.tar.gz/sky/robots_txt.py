import re

robots_txt = '...'
user_agent_found = False
crawl_filter_regexps = []
crawl_required_regexps = []
for line in robots_txt.split():
    line.strip()
    if line.startswith('#'):
        continue
    if line.startswith('User-agent:'):
        if '*' in line:
            user_agent_found = True
        else:
            user_agent_found = False
    elif user_agent_found:
        if line.startswith('Disallow'):
            res = line.split('Disallow:')
            if res:
                res = res[1:]
                if res == '*':
                    raise ValueError("robots.txt disallows bot to crawl anything.")
            crawl_filter_str = re.escape(line.split('Disallow: ', ))
