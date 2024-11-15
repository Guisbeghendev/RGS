# Generated by Django 5.1.2 on 2024-10-15 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticad', '0003_customuser_age_customuser_avatar_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Os grupos aos quais este usuário pertence.', related_name='customuser_set', to='auth.group', verbose_name='grupos'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Permissões específicas para este usuário.', related_name='customuser_set', to='auth.permission', verbose_name='permissões de usuário'),
        ),
    ]
