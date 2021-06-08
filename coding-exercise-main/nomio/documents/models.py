from django.db import models

class LegalDoc(models.Model):
     doc = models.FileField(upload_to='')
     up_date = models.DateField(auto_now_add=True)
