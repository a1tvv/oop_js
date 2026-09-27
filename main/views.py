from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.management import call_command

from .models import Card


def index(request):
    cards = Card.objects.filter(is_active=True)
    return render(request, 'index.html', {'cards': cards})


def admin_info(request):
    admin_data = {
        'name': 'Группа разработчиков проекта «Свет Сунны»',
        'email': 'alraiabdurahim07@gmail.com',
        'telegram': 'https://t.me/dusi84',
        'youtube': 'https://youtube.com/@abdurtwhd',
        'about': 'По всем вопросам пишите в Telegram. '
                 'Проект не нуждается в финансировании, достаточно просто поделиться ссылкой с близкими.',
    }
    return render(request, 'admin_info.html', {'admin': admin_data})


def latest_video(request):
    """Возвращает ID последнего YouTube-видео (для уведомлений)."""
    card = Card.objects.filter(card_type='youtube').order_by('-id').first()
    if card:
        return JsonResponse({
            'id': card.url,
            'title': card.title,
            'url': card.url,
            'image': card.get_image(),
        })
    return JsonResponse({'id': None})


def sira(request):
    return render(request, 'sira.html')


def riyad_useimin(request):
    return render(request, 'riyad_useimin.html')


def tafsir(request):
    return render(request, 'tafsir.html')


def cron_parse_youtube(request):
    """Endpoint для Vercel Cron: запускает парсер YouTube."""
    auth = request.headers.get('Authorization', '')
    expected = f'Bearer {settings.CRON_SECRET}'

    if not settings.CRON_SECRET or auth != expected:
        return JsonResponse({'error': 'forbidden'}, status=403)

    try:
        call_command('parse_youtube')
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)