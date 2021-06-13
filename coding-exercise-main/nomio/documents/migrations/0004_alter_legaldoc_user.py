# Generated by Django 3.2.3 on 2021-06-13 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0003_alter_legaldoc_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legaldoc',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
