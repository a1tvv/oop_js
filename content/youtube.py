"""
Получение последнего видео с YouTube-канала через публичный RSS-фид.
Не требует API-ключа YouTube Data API.
"""
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

ATOM_NS = '{http://www.w3.org/2005/Atom}'
YT_NS = '{http://www.youtube.com/xml/schemas/2015}'

FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'


def fetch_latest_video(channel_id):
    """
    Возвращает dict с данными о последнем видео канала:
    {'video_id', 'title', 'url', 'published_at'} (published_at — строка ISO 8601).
    Возвращает None, если channel_id не задан, канал недоступен
    или фид пустой/битый.
    """
    if not channel_id:
        return None

    request = urllib.request.Request(
        FEED_URL.format(channel_id=channel_id),
        headers={'User-Agent': 'Mozilla/5.0 (compatible; NurAsSunnahBot/1.0)'},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read()
    except (urllib.error.URLError, TimeoutError):
        return None

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return None

    entry = root.find(f'{ATOM_NS}entry')
    if entry is None:
        return None

    video_id_el = entry.find(f'{YT_NS}videoId')
    title_el = entry.find(f'{ATOM_NS}title')
    published_el = entry.find(f'{ATOM_NS}published')
    link_el = entry.find(f'{ATOM_NS}link')

    if video_id_el is None or video_id_el.text is None or published_el is None:
        return None

    video_id = video_id_el.text
    url = link_el.get('href') if link_el is not None else f'https://www.youtube.com/watch?v={video_id}'

    return {
        'video_id': video_id,
        'title': title_el.text if title_el is not None else '',
        'url': url,
        'published_at': published_el.text,
    }