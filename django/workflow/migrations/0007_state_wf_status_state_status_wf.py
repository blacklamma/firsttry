# Generated by Django 4.2.1 on 2023-06-17 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_status_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='wf',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workflow.workflow'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workflow.state'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='wf',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workflow.workflow'),
            preserve_default=False,
        ),
    ]
