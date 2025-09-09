from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Source(models.Model):
    SOURCE_TYPES = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('series', 'Сериал'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    type = models.CharField(max_length=10, choices=SOURCE_TYPES, verbose_name="Тип")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"


class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты")
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name="Источник")
    weight = models.PositiveIntegerField(default=1, verbose_name="Вес")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['text', 'source']

    def __str__(self):
        return f"{self.text[:50]}... ({self.source})"