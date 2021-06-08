from django.contrib.auth.models import User
from django.db import models


class LegalDoc(models.Model):
     doc = models.FileField(upload_to='')
     up_date = models.DateField(auto_now_add=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

     def __str__(self):
          return " ".join([self.doc.name, str(self.user), str(self.up_date)])
