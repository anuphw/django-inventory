# Generated by Django 4.1.2 on 2022-11-24 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0004_clientcontact_created_at_clientcontact_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('delivary_address', models.CharField(default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='clients.client')),
                ('contact_person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='clients.clientcontact')),
            ],
            options={
                'verbose_name_plural': '2. Deals',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Inquiry'), ('2', 'Quotation Sent'), ('3', 'Negotation'), ('4', 'Processing'), ('5', 'Delivering'), ('6', 'Delivered'), ('7', 'Complete')], max_length=20)),
            ],
            options={
                'verbose_name_plural': '1. Statuses',
            },
        ),
        migrations.CreateModel(
            name='ProjectTimeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.status')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '3. Project Timeline',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.status'),
        ),
    ]
