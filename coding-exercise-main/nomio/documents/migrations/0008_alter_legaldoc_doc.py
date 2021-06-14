# Generated by Django 3.2.3 on 2021-06-14 10:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_alter_legaldoc_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legaldoc',
            name='doc',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(['doc', 'docx', 'img', 'jpg', 'pdf', 'png'])]),
        ),
    ]
