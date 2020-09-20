# Generated by Django 3.1 on 2020-09-16 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_name', models.CharField(max_length=100, verbose_name='Стихия')),
            ],
        ),
        migrations.CreateModel(
            name='ExpPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField()),
                ('img', models.ImageField(default='no-image.png', upload_to='skill_image')),
                ('level', models.IntegerField(null=True)),
                ('element', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.element')),
            ],
        ),
        migrations.AlterField(
            model_name='typeattack',
            name='type',
            field=models.CharField(max_length=100, verbose_name='Тип атаки'),
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weapon_name', models.CharField(max_length=100, verbose_name='Оружие')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.typeattack')),
            ],
        ),
        migrations.CreateModel(
            name='UserSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activate', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('skill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.skill')),
            ],
        ),
        migrations.CreateModel(
            name='UserPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.userskills')),
                ('points', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.exppoints')),
            ],
        ),
        migrations.CreateModel(
            name='SkillsRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='higher', to='skills.skill')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.skill')),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='weapon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skills.weapon'),
        ),
    ]