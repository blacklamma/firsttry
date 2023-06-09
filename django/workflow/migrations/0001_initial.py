# Generated by Django 4.2.1 on 2023-06-12 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailToTicketConf',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email_id', models.EmailField(max_length=255)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('smtp_host_port', models.IntegerField()),
                ('email_server', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tbl_email_to_ticket_conf',
            },
        ),
        migrations.CreateModel(
            name='IncomingEmails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, 'Pending'), (2, 'Processing'), (3, 'Processed'), (-3, 'Error')], default=1)),
                ('from_address', models.EmailField(blank=True, max_length=250, null=True)),
                ('subject', models.CharField(max_length=1000)),
                ('content', models.TextField(blank=True, null=True)),
                ('attached_files', models.CharField(blank=True, max_length=500, null=True)),
                ('received_time', models.DateTimeField(blank=True, null=True)),
                ('convert_time', models.DateTimeField(blank=True, null=True)),
                ('is_converted', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tbl_incoming_emails',
            },
        ),
        migrations.CreateModel(
            name='OutgoingEmails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, 'Pending'), (2, 'Processing'), (3, 'Success'), (4, 'Delivered'), (-3, 'Error')], default=1)),
                ('to_address', models.TextField()),
                ('cc_address', models.TextField(blank=True, null=True)),
                ('bcc_address', models.TextField(blank=True, null=True)),
                ('from_address', models.EmailField(blank=True, max_length=250, null=True)),
                ('subject', models.CharField(max_length=1000)),
                ('content', models.TextField(blank=True, null=True)),
                ('attached_files', models.CharField(blank=True, max_length=500, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('queue_time', models.DateTimeField(blank=True, null=True)),
                ('sent_time', models.DateTimeField(blank=True, null=True)),
                ('header_message', models.TextField(blank=True, null=True)),
                ('footer_message', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_outgoing_emails',
            },
        ),
        migrations.CreateModel(
            name='SMTPConf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=100)),
                ('host_username', models.CharField(max_length=1000)),
                ('host_password', models.CharField(max_length=1000)),
                ('host_email', models.CharField(max_length=1000)),
                ('host_port', models.IntegerField(default=465)),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tbl_smtp_conf',
            },
        ),
    ]
