# Generated by Django 4.0.3 on 2022-04-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books_management", "0003_alter_book_pages_alter_book_published_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="pages",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="book",
            name="published_date",
            field=models.IntegerField(default=0),
        ),
    ]
