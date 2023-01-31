# Generated by Django 3.2.16 on 2023-01-31 14:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.FloatField(default=0.0, null=True)),
                ('doj', models.DateField(blank=True, null=True)),
                ('working_status', models.CharField(choices=[('WORKING', 'WORKING'), ('PAUSE', 'PAUSE')], default='WORKING', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MonthWageGiven',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(blank=True, default=0.0)),
                ('pre_amount', models.FloatField(blank=True, default=0.0)),
                ('month', models.CharField(blank=True, max_length=10)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_wage', to='khataApp.worker')),
            ],
        ),
        migrations.CreateModel(
            name='DailyWage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('type', models.CharField(choices=[('SPEND', 'SPEND'), ('GIVEN', 'GIVEN')], default='SPEND', max_length=50)),
                ('reason', models.CharField(blank=True, default='-', max_length=255, null=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_wage', to='khataApp.worker')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.BigIntegerField(unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
