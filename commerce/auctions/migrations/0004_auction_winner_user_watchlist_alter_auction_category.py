# Generated by Django 4.0.2 on 2022-03-14 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_image_href'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auctions_won', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='User', to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('tech', 'technical'), ('fashion', 'fashion'), ('toy', 'toys'), ('furniture', 'furniture'), ('livestyle', 'livestyle')], max_length=16),
        ),
    ]
