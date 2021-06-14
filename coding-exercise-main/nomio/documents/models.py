from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class LegalDoc(models.Model):
    """Create a LegalDoc model."""

    allowed_extensions = ["doc", "docx", "img", "jpg", "pdf", "png"]
    doc = models.FileField(validators=[FileExtensionValidator(allowed_extensions)])
    up_date = models.DateField(auto_now_add=True)

    # use RESTRICT to avoid unintended data loss
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    class Meta:
        # avoids pagination ordering warnings
        ordering = ["-up_date"]

    def __str__(self):
        """
        Returns:
            str: Filename, name of user and upload date.
        """
        return " ".join([self.doc.name, str(self.user), str(self.up_date)])
