from django.db import migrations, models
import applications.storage
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0002_alter_application_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='year',
            field=models.CharField(
                choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year')],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.FileField(
                blank=True,
                storage=applications.storage.PrivateResumeStorage(),
                upload_to='',
                validators=[django.core.validators.FileExtensionValidator(['pdf'])],
            ),
        ),
    ]
