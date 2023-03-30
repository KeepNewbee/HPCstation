from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class DocumentPost(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE )

    title = models.CharField(max_length=100 )

    body = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    doc_type = models.CharField(max_length=100)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
        