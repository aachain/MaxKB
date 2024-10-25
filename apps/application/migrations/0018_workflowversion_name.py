# Generated by Django 4.2.15 on 2024-10-16 15:17

from django.db import migrations, models

sql = """
UPDATE "public".application_work_flow_version
SET "name" =  TO_CHAR(create_time, 'YYYY-MM-DD HH24:MI:SS');
"""


class Migration(migrations.Migration):
    dependencies = [
        ('application', '0017_application_tts_model_params_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='clean_time',
            field=models.IntegerField(default=180, verbose_name='清理时间'),
        ),
        migrations.AddField(
            model_name='workflowversion',
            name='name',
            field=models.CharField(default='', max_length=128, verbose_name='版本名称'),
        ),
        migrations.RunSQL(sql),
        migrations.AddField(
            model_name='workflowversion',
            name='publish_user_id',
            field=models.UUIDField(default=None, null=True, verbose_name='发布者id'),
        ),
        migrations.AddField(
            model_name='workflowversion',
            name='publish_user_name',
            field=models.CharField(default='', max_length=128, verbose_name='发布者名称'),
        ),
    ]