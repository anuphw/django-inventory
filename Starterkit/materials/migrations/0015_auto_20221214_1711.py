# Generated by Django 3.2.16 on 2022-12-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0014_auto_20221212_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='inventoryadjustment',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='materialqty',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='materialreturn',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='materialtransfer',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='units',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
