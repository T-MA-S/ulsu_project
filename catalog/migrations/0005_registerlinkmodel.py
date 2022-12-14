# Generated by Django 4.1.2 on 2022-12-12 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_usermodel_boards'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterlinkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=128, null=True)),
                ('expired_date', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('username', models.TextField()),
                ('password', models.TextField()),
            ],
            options={
                'verbose_name': 'Ссылка для регистрации',
                'verbose_name_plural': 'Ссылки для регистрации',
            },
        ),
    ]
