# Generated by Django 3.2.4 on 2021-06-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='is_borrower',
            field=models.BooleanField(default=False, verbose_name='Borrower'),
        ),
        migrations.AddField(
            model_name='balance',
            name='is_investor',
            field=models.BooleanField(default=False, verbose_name='Investor '),
        ),
    ]
