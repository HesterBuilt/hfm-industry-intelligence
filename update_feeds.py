"""Fetch Google News RSS search feeds and publish a small static JSON file."""
import calendar
import datetime as dt
import json
import re
import time
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlencode
import feedparser
import requests

QUERIES = {
    'North Georgia': ['Gainesville GA development construction housing', 'Hall County Georgia building permits development', 'Braselton Flowery Branch Georgia new homes business'],
    'Housing & Remodeling': ['home remodeling demand US housing market', 'NAHB home builder remodeling index', 'mortgage rates renovation spending'],
    'Cabinetry & Materials': ['cabinet manufacturing woodworking industry', 'cabinet hardware plywood lumber prices tariffs', 'kitchen cabinetry supply chain'],
    'Design': ['kitchen design trends cabinetry NKBA Houzz', 'interior design kitchen storage built ins'],
    'Marketing & SEO': ['Google local search business profile updates', 'Instagram Facebook Pinterest marketing changes small business'],
    'Business & Regulation': ['Georgia small business construction regulations', 'US construction labor costs tariffs building materials'],
}

def fetch(query):
    url = 'https://news.google.com/rss/search?' + urlencode({'q': query, 'hl':'en-US','gl':'US','ceid':'US:en'})
    response = requests.get(url, timeout=22, headers={'User-Agent':'HFM-Industry-Intelligence/1.0 (+https://hesterfamilymillwork.com)'})
    response.raise_for_status()
    return feedparser.parse(response.content).entries

def date_of(entry):
    parsed = entry.get('published_parsed') or entry.get('updated_parsed')
    if parsed:
        return dt.datetime.fromtimestamp(calendar.timegm(parsed), dt.timezone.utc)
    return dt.datetime.now(dt.timezone.utc)

def main():
    now = dt.datetime.now(dt.timezone.utc)
    seen = set()
    items = []
    errors = []
    for category, queries in QUERIES.items():
        for query in queries:
            try:
                entries = fetch(query)
                for e in entries[:15]:
                    title = re.sub(r'\s+', ' ', e.get('title', '')).strip()
                    link = e.get('link', '')
                    if not title or not link or not link.startswith('https://'):
                        continue
                    key = re.sub(r'\W+', '', title.lower())[:100]
                    if key in seen:
                        continue
                    published = date_of(e)
                    if (now-published).days > 45:
                        continue
                    seen.add(key)
                    source = e.get('source', {}).get('title') if isinstance(e.get('source'), dict) else None
                    if not source and ' - ' in title:
                        title, source = title.rsplit(' - ', 1)
                    items.append({'category':category,'title':title,'source':source or 'News source','url':link,'published':published.isoformat()})
            except Exception as exc:
                errors.append(f'{category}: {query}: {exc}')
            time.sleep(.25)
    items.sort(key=lambda a:a['published'],reverse=True)
    result = {'updated':now.isoformat(),'articles':items[:150]}
    if not items:
        raise RuntimeError('No feeds succeeded; refusing to overwrite news.json. '+str(errors[:3]))
    Path(__file__).with_name('news.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(result["articles"])} articles; {len(errors)} failed searches')
    for err in errors[:10]: print('WARN',err)

if __name__=='__main__': main()
