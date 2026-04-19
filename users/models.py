from django.db import models
from django.contrib.auth.models import User


class CodeConfirmation(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='confirmation_code'
                                )
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.user.username}: {self.code}'