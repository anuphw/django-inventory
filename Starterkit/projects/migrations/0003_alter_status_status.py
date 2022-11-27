# Generated by Django 3.2.16 on 2022-11-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_deal_projecttimeline_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[('1', 'Inquiry'), ('2', 'Quotation Sent'), ('3', 'Negotation'), ('4', 'Processing'), ('5', 'Delivering'), ('6', 'Delivered'), ('7', 'Complete'), ('8', 'Cancelled')], max_length=20),
        ),
    ]
