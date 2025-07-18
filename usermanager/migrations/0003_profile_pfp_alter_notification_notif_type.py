# Generated by Django 5.2.2 on 2025-07-05 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to='pfps/'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('friend_request', 'Friend Request'), ('friend_accept', 'Friend Request Accepted'), ('post_like', 'Post Like'), ('comment_like', 'Comment Like'), ('post_comment', 'Post Comment'), ('post_share', 'Post Share')], max_length=20),
        ),
    ]
