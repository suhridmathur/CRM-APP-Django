# Generated by Django 3.0.6 on 2020-11-01 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_leadorder_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='deal',
        ),
        migrations.AddField(
            model_name='deal',
            name='Date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='collection_terms',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='company_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='deal_no',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='delivery_days',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='delivery_to',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='discount',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='grand_total',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='muncipality',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='notes',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='order_no',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='order_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='payment_terms',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='poboxno',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='postoffice',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='price',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='product',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='qty',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='sales_person',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='street',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='sub_total',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='tel_phone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='total',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='transport_charge',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='vat',
            field=models.CharField(max_length=200, null=True),
        ),
    ]