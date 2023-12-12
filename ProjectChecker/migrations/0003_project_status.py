# Generated by Django 4.1.7 on 2023-12-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectChecker', '0002_customuser_staff_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('approved', 'approved'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=100),
        ),
    ]
