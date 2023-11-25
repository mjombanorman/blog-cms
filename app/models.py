from django.db import models
from django.utils.text import slugify

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
   
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        return super(Post,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    
    
