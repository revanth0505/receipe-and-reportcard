# Generated by Django 4.2.3 on 2023-07-13 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0005_reportcard'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reportcard',
            unique_together={('student_rank', 'date_of_report')},
        ),
    ]