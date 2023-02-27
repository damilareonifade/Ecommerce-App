# Generated by Django 4.1.5 on 2023-02-25 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_state_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressglobal',
            name='price',
            field=models.IntegerField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='addressglobal',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_state', to='accounts.state'),
        ),
    ]
