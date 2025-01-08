from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
import uuid


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='articles')
    image = models.ImageField(upload_to='images/')
    posted_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if Article.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super(Article, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse(
            'articles:detail',
            kwargs={
                'year':self.posted_at.year,
                'month':self.posted_at.month,
                'day':self.posted_at.day,
                'slug':self.slug,
            }
        )

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(unique=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField()