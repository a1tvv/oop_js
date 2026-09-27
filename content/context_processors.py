from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import FeaturedVideo


def featured_video(request):
    """
    Кладёт в контекст каждого шаблона последнее видео с канала,
    если оно опубликовано не позже NEW_VIDEO_DISPLAY_DAYS назад.
    Если подходящего видео нет — featured_video будет None,
    и баннер в base.html просто не отрисуется.
    """
    cutoff = timezone.now() - timedelta(days=settings.NEW_VIDEO_DISPLAY_DAYS)
    video = (
        FeaturedVideo.objects.filter(published_at__gte=cutoff)
        .order_by('-published_at')
        .first()
    )
    return {'featured_video': video}