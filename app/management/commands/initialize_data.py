from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from app.models import Post, Tag, User, Profile, Subscribe, Comment

fake = Faker()


class Command(BaseCommand):
    help = 'Generate Fake Data for all the system tables'

    def handle(self, *args, **kwargs):
        # Generate Tags
        self.generate_tags()

        # Generate Users and Profiles
        self.generate_profiles()

        # Generate Subscriptions
        self.generate_subscriptions()

        # Generate Posts, Comments, and Replies
        self.generate_posts()

    # Generate Tags
    def generate_tags(self):
        self.stdout.write(f'Generating Tags...')
        for i in range(12):
            Tag.objects.create(name=fake.word(), description=fake.paragraph())
        self.stdout.write(self.style.SUCCESS('Successfully generated tags.'))

    # Generate Users and Profiles
    def generate_profiles(self):
        self.stdout.write(f'Generating Users and Profiles...')
        for i in range(15):
            user = User.objects.create_user(
                username=fake.name(), email=fake.email(), password=fake.password())
            Profile.objects.create(
                user=user,
                bio=fake.paragraph(),
                location=fake.city()
            )
        self.stdout.write(self.style.SUCCESS(
            'Successfully generated users and profiles.'))

    # Generate Subscriptions
    def generate_subscriptions(self):
        self.stdout.write(f'Generating Subscriptions...')
        for i in range(15):
            user = User.objects.order_by('?').first()  # Select a random user
            Subscribe.objects.create(email=user.email)
        self.stdout.write(self.style.SUCCESS(
            'Successfully generated subscriptions.'))

    # Generate Posts, Comments, and Replies
    def generate_posts(self):
        self.stdout.write(f'Generating Posts, Comments, and Replies...')
        for i in range(100):
            user = User.objects.order_by('?').first()  # Select a random user
            post = Post.objects.create(
                title=fake.sentence(nb_words=5),
                content=fake.paragraph(nb_sentences=15),
                last_update=fake.date_time_this_year(),
                slug=slugify(fake.sentence(nb_words=5)),
                image=fake.image_url(),
                view_count=fake.random_int(min=0, max=1000),
                is_featured=fake.boolean(),
                author=user
            )

            # Add random tags to the post
            tags = Tag.objects.order_by('?')[:4]  # Select 3 random tags
            post.tags.set(tags)

            # Generate Comments
            for j in range(4):
                comment = Comment.objects.create(
                    content=fake.paragraph(nb_sentences=15),
                    date=fake.date_time_this_year(),
                    name=fake.name(),
                    email=fake.email(),
                    website=fake.url(),
                    post=post,
                    author=user
                )

                # Generate Replies
                for k in range(3):
                    Comment.objects.create(
                        content=fake.paragraph(nb_sentences=15),
                        date=fake.date_time_this_year(),
                        name=fake.name(),
                        email=fake.email(),
                        website=fake.url(),
                        post=post,
                        author=user,
                        parent=comment
                    )

        self.stdout.write(self.style.SUCCESS(
            'Successfully generated posts, comments, and replies.'))
