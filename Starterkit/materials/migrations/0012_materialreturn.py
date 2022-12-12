# Generated by Django 3.2.16 on 2022-12-12 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_project_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0011_materialqty_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialReturn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='materials.warehouse')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='materials.inventory')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
