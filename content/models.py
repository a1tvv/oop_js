from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    audio_file = models.FileField(upload_to='audio/', verbose_name="Аудиофайл")

    def __str__(self):
        return self.title


class RiyadhAsSalihin(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")

    audio_url = models.URLField(
        max_length=500,
        verbose_name="Ссылка на аудио (S3)",
        null=True,
        blank=True
    )

    description = models.TextField(verbose_name="Описание/Вопросы", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Урок Рияд ас-Салихин"
        verbose_name_plural = "Уроки Рияд ас-Салихин"

    def __str__(self):
        return self.title


class FeaturedVideo(models.Model):
    video_id = models.CharField(max_length=32, unique=True, verbose_name="ID видео на YouTube")
    title = models.CharField(max_length=255, verbose_name="Название")
    url = models.URLField(verbose_name="Ссылка на видео")
    published_at = models.DateTimeField(verbose_name="Дата публикации на YouTube")
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name="Когда сайт заметил видео")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Новое видео (YouTube)"
        verbose_name_plural = "Новые видео (YouTube)"

    def __str__(self):
        return self.title