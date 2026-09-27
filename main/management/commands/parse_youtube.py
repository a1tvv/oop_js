import re
import feedparser
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from main.models import Card


def clean_title(title: str) -> str:
    """Убирает эмодзи и лишние пробелы в начале заголовка."""
    # Убираем эмодзи в начале строки
    title = re.sub(r'^[\U0001F300-\U0001FAFF\U00002600-\U000027BF\s]+', '', title)
    return title.strip()


class Command(BaseCommand):
    help = 'Парсит последние видео с YouTube-канала через RSS и создаёт карточки'

    def handle(self, *args, **options):
        channel_id = getattr(settings, 'YOUTUBE_CHANNEL_ID', '')
        if not channel_id:
            self.stdout.write(self.style.ERROR(
                'YOUTUBE_CHANNEL_ID не задан в settings / .env'
            ))
            return

        rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
        self.stdout.write(f'Загружаю RSS: {rss_url}')

        feed = feedparser.parse(rss_url)

        if not feed.entries:
            self.stdout.write(self.style.ERROR('RSS пустой. Проверьте channel_id.'))
            return

        new_count = 0
        for entry in feed.entries:
            video_id = entry.id.split(':')[-1]
            url = entry.link

            if Card.objects.filter(url=url).exists():
                continue

            if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                thumbnail_url = entry.media_thumbnail[0]['url']
            else:
                thumbnail_url = f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'

            published_dt = parse_datetime(entry.published)
            published_date = published_dt.date() if published_dt else timezone.now().date()

            Card.objects.create(
                title=clean_title(entry.title),
                description='Новое видео на канале «К Исламу»',
                image_url=thumbnail_url,
                url=url,
                card_type='youtube',
                order=0,
                is_active=True,
                published=published_date,
            )
            new_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово. Добавлено новых видео: {new_count}. '
            f'Всего карточек в БД: {Card.objects.count()}'
        ))