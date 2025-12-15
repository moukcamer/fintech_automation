from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_transaction_created_at_alter_transaction_issued_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='issued_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
