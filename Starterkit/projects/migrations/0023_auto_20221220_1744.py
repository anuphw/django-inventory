# Generated by Django 3.2.16 on 2022-12-20 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_deliveryproduct_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryproduct',
            name='notes',
        ),
        migrations.AddField(
            model_name='productreturn',
            name='notes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
