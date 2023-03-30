from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(decimal_places=6, max_digits=8, null=True, blank=True)
    lng = models.DecimalField(decimal_places=6, max_digits=8, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class User(models.Model):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE = [(MEMBER, "Пользователь"), (MODERATOR, "Модератор"), (ADMIN, "Администратор")]

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=ROLE)
    age = models.PositiveSmallIntegerField()
    location = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]
