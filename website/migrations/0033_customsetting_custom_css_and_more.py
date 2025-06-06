# Generated by Django 4.1.10 on 2023-12-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0032_locationpage_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='customsetting',
            name='custom_css',
            field=models.TextField(help_text='Custom CSS', null=True, verbose_name='Custom CSS'),
        ),
        migrations.AlterField(
            model_name='locationmarker',
            name='description',
            field=models.CharField(default='', max_length=255, verbose_name='Address'),
        ),
    ]
