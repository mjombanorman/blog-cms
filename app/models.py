from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True,max_length=200)
    image = models.ImageField(upload_to='post-images/',null=True,blank=True)

    def __str__(self):
        return self.title