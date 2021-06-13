from django.contrib.auth.models import User
from django.db import models


class LegalDoc(models.Model):
    doc = models.FileField()
    up_date = models.DateField(auto_now_add=True)

    # use RESTRICT to avoid unintended data loss
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    class Meta:
        # this orders the database and avoids pagination ordering warnings
        ordering = ["-up_date"]

    def __str__(self):
        return " ".join([self.doc.name, str(self.user), str(self.up_date)])
