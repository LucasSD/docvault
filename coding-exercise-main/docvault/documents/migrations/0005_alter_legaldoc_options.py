# Generated by Django 3.2.3 on 2021-06-13 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_alter_legaldoc_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legaldoc',
            options={'ordering': ['up_date']},
        ),
    ]
