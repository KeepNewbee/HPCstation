from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class TutorialPost(models.Model):
    
    author = models.CharField(max_length=100 )

    title = models.CharField(max_length=100 )

    body = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    doc_type = models.CharField(max_length=100)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tutorial:tutorial_detail', args={self.id})