# Generated by Django 4.1 on 2023-03-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0005_profile_is_engineer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="college",
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name="profile",
            name="department",
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name="profile",
            name="position",
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name="profile",
            name="real_name",
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
