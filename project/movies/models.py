from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название жанра', null=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Actor(models.Model):
    name = models.CharField(max_length=64, verbose_name="Имя актёра")

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Актёр"
        verbose_name_plural = "Актёры"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=256, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.user.username} profile"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class Movie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, verbose_name='жанр', null=True)
    title = models.CharField(max_length=64, verbose_name='Название фильма', null=True, unique=False, help_text='Какая-то полезная информация о названии фильма.')
    description = models.TextField(verbose_name="Описание", blank=True, default="")
    added_at = models.DateTimeField(verbose_name='Дата добавления', default=timezone.now)
    year = models.IntegerField(verbose_name='Год', null=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)
    favorited_by = models.ManyToManyField(User, related_name="favorite_movies", blank=True)

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.genre.name}"

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ('added_at',)
