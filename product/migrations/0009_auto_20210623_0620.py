# Generated by Django 3.1.7 on 2021-06-23 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]
