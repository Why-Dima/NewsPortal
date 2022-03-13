from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_users = models.FloatField(default=1.0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(postsRating=Sum('rating_post'))
        p_r = 0
        p_r += posts_rating.get('postsRating')

        comments_rating = self.users.comment_set.aggregate(commentRating=Sum('rating_comment'))
        c_r = 0
        c_r += comments_rating.get('commentRating')

        self.rating_users = p_r * 3
        self.save()

    def __str__(self):
        return f'{self.users}'


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, )

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):

    news = 'NE'
    paper = 'PA'

    POSITIONS = [(news, "Новости"), (paper, "Статьи")]

    authors = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор', default="Dima")
    # categories = models.ManyToManyField(Category, through='PostCategory')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name= 'Категория(categories)')
    time_in = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating_post = models.FloatField(default=1.0)
    paper_news = models.CharField(max_length=2, choices=POSITIONS, default=news)

    def comment_like(self):
        self.rating_post += 1.0
        self.save()

    def comment_dislike(self):
        self.rating_post -= 1.0
        self.save()

    def preview(self):
        self.text = f'{self.text[:124]}...'
        return self.text

    def get_absolute_url(self):
        return f'/news/{self.id}'


# class PostCategory(models.Model):
#     posts = models.ForeignKey(Post, on_delete=models.CASCADE)
#     categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    text_commit = models.CharField(max_length=255)
    commit_in_time = models.DateTimeField(auto_now_add=True)
    rating_comment = models.FloatField(default=1.0)

    def comment_like(self):
        self.rating_comment += 1.0
        self.save()

    def comment_dislike(self):
        self.rating_comment -= 1.0
        self.save()
