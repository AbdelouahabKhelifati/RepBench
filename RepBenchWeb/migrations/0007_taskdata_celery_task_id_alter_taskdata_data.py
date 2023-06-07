# Generated by Django 4.2 on 2023-05-16 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RepBenchWeb', '0006_taskdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdata',
            name='celery_task_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='taskdata',
            name='data',
            field=models.JSONField(default=list),
        ),
    ]