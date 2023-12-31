# Generated by Django 4.1.4 on 2023-01-01 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('dataframe', models.JSONField()),
                ('ref_url', models.CharField(blank=True, max_length=200, null=True)),
                ('url_text', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('additional_info', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='InjectedContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('injectedContainer_json', models.JSONField()),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('info', models.JSONField(null=True)),
            ],
        ),
    ]
