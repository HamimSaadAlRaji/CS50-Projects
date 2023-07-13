# Generated by Django 4.2.2 on 2023-07-13 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_watchlist_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]