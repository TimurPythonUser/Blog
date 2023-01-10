from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название статьи')
    category = models.CharField(max_length=100, verbose_name='Тема статьи')
    picture = models.ImageField(null=True, verbose_name='Картинка')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name='Автор статьи', related_name='my_posts')
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comments(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}'


