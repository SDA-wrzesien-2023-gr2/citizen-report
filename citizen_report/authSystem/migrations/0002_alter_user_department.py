# Generated by Django 4.2.5 on 2023-09-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(choices=[('APP', 'Applicant'), ('SYS', 'System supervisor'), ('RBR', 'Roads and bridges'), ('SWS', 'Sewer and waterworks'), ('POW', 'Power supply'), ('GAS', 'Gasworks'), ('TEL', 'Telecommunication'), ('GAR', 'Garbage disposal'), ('CTR', 'City transport'), ('HTH', 'Healthcare'), ('EDU', 'Education'), ('SAF', 'Public safety')], default='APP', max_length=100),
        ),
    ]
