# Generated by Django 3.1.6 on 2021-03-08 07:46

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_comment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name=users.models.Profile),
        ),
    ]
