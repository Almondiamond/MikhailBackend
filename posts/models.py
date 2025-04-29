from django.contrib import admin
from django.db import models


class Post(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='media')
    created_by = models.ForeignKey('core.Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


admin.site.register(Post)

