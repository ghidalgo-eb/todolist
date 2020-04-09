from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Priority(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField()

    def __str__(self):
        return '{} - {} (order {})'.format(
            self.id,
            self.name,
            self.order,
        )


class TodoList(models.Model):
    title = models.CharField(max_length=20)
    Description = models.CharField(max_length=60)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    done = models.BooleanField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)



