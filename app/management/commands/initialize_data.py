from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from datetime import timedelta
from app.models import Post
from django.template.defaultfilters import slugify


class Command(BaseCommand):
    help = 'Generate Fake Data for all the system tables'

    def handle(self, *args, **kwargs):
        self.generate_posts()
   
    def generate_posts(self):
        self.stdout.write(f'Generating Posts...')
        fake = Faker()
        for _ in range(30):
            title = fake.sentence(nb_words=5)
            content = fake.paragraph(nb_sentences=15)
            last_update = fake.date_time_this_year()
            slug = slugify(title)
            
            Post.objects.bulk_create([Post(title=title, content=content, last_update=last_update, slug=slug)])
  
        self.stdout.write(self.style.SUCCESS(
            'Successfully bookings for all customers.'))
