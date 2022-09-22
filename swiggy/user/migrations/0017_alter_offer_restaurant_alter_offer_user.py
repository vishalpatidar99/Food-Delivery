# Generated by Django 4.1 on 2022-09-02 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_alter_restaurant_followers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0016_alter_offer_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]