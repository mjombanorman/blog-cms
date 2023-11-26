from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,max_length=100)
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        return super(Tag,self).save(*args,**kwargs)

    def __str__(self):
        return self.name
    
    

        
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True,max_length=200)
    image = models.ImageField(upload_to='post-images/',null=True,blank=True)
    tags = models.ManyToManyField(Tag,blank=True,related_name="post")
    view_count = models.IntegerField(null=True,blank=True)
   
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        return super(Post,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    

class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='replies')
