# Generated by Django 2.1 on 2019-03-31 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('orderedfrom', models.CharField(max_length=50)),
                ('productid', models.IntegerField()),
                ('taken', models.BooleanField(default=False)),
            ],
        ),
    ]
