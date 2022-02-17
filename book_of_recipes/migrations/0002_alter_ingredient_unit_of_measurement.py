# Generated by Django 3.2.9 on 2022-02-17 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_of_recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit_of_measurement',
            field=models.CharField(choices=[('KG', 'кг'), ('G', 'г'), ('L', 'л'), ('ML', 'мл'), ('P', 'шт.'), ('T', 'ч.л.'), ('EMPTY', '')], max_length=2, verbose_name='Единица измерения'),
        ),
    ]