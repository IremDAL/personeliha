# Generated by Django 5.1.4 on 2024-12-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='partsadd',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('team', models.CharField(max_length=50)),
                ('aircraft', models.CharField(max_length=50)),
                ('parts', models.CharField(max_length=50)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='personeladd',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('team', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ucaklar',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('aircraft', models.CharField(max_length=50, unique=True)),
                ('partss', models.TextField(default='[]')),
            ],
        ),
        migrations.CreateModel(
            name='ucakparcasayilari',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('ucak_adi', models.CharField(max_length=50, unique=True)),
                ('kanat_sayisi', models.IntegerField(default=0)),
                ('kuyruk_sayisi', models.IntegerField(default=0)),
                ('govde_sayisi', models.IntegerField(default=0)),
                ('aviyonik_sayisi', models.IntegerField(default=0)),
            ],
        ),
    ]
