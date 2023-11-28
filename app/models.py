from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile-images/',null=True,blank=True)
    slug = models.SlugField(unique=True,max_length=100)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.user.first_name + self.user.last_name)
        return super(Profile,self).save(*args,**kwargs)

    def __str__(self):
        return self.user.username
    
    @property
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name
class Subscribe(models.Model):
    email = models.EmailField(max_length=254)
    date = models.DateTimeField(auto_now=True)
    
    
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
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
   
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
    
    
    def __str__(self):
        #Substring to the first 4 words of content
        title = self.content[:33]
        return title
    
