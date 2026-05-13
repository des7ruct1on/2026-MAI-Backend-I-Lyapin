from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_profile_user_onetoone"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
    ]
