from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='issued_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-12-05 00:00'),
            preserve_default=False,
        ),
    ]
