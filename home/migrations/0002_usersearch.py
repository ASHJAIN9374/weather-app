# Generated by Django 5.0.6 on 2024-06-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=300)),
                ('date', models.DateField()),
            ],
            options={
                'unique_together': {('username', 'city')},
            },
        ),
    ]
