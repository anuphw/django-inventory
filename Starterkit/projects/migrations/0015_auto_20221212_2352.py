# Generated by Django 3.2.16 on 2022-12-12 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_project_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='delivary_address',
            new_name='delivery_address',
        ),
        migrations.AlterField(
            model_name='projecttimeline',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.status'),
        ),
    ]
