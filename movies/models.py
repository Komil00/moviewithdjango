from datetime import date

from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Категория",max_length=155)
    description = models.TextField("Описания")
    url = models.SlugField(max_length=155)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Actor(models.Model):
    name = models.CharField("Name",max_length=155)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Описания")
    image = models.ImageField("Images",upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})

    class Meta:
        verbose_name = 'Actor and rejisor'
        verbose_name_plural = 'Actors and rejisors'

class Genre(models.Model):
    name = models.CharField("Name", max_length=133)
    description = models.TextField("Описания")
    url = models.SlugField(max_length=155,unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Ganre'
        verbose_name_plural = 'Ganres'

class Movie(models.Model):
    title = models.CharField("Name",max_length=122)
    tagline = models.CharField("Слоган", max_length=122, default='')
    description = models.TextField("Описания")
    poster = models.ImageField("Постер", upload_to='movies/')
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Country", max_length=45)
    directors = models.ManyToManyField(Actor, verbose_name="rejisor", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actors", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="ganres")
    world_premiere = models.DateField("Дата примера", default=date.today)
    budget= models.PositiveIntegerField("Budget", default=0,help_text="show price to dollars")
    fees_in_usa = models.PositiveIntegerField("Сбори в США", default=0,help_text="show price to dollars")
    fees_in_world = models.PositiveIntegerField("Сбори в мире", default=0, help_text="show price to dollars")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=133,unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieShots(models.Model):
    title = models.CharField("Name", max_length=122)
    description = models.TextField("Описания")
    image = models.ImageField("Images", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из Фыльма'
        verbose_name_plural = 'Кадри из Фыльма'

class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField("Значение", default=0)
    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ["-value"]

class Rating(models.Model):
    ip = models.CharField("IP adress", max_length=133)
    star = models.ForeignKey(RatingStar,on_delete=models.CASCADE,verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'


class Reviews(models.Model):
    email = models.EmailField(max_length=133)
    name = models.CharField("Name", max_length=133)
    text = models.TextField("Sms", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True,null=True)
    movie = models.ForeignKey(Movie, verbose_name="film", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
