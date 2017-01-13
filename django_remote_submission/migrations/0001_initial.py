# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 18:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_remote_submission.models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interpreter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(help_text='The human-readable name of the interpreter', max_length=100, verbose_name='Interpreter Name')),
                ('path', models.CharField(help_text='The full path of the interpreter path.', max_length=256, verbose_name='Command Full Path')),
                ('arguments', django_remote_submission.models.ListField(help_text='The arguments used when running the interpreter', max_length=256, verbose_name='Command Arguments')),
            ],
            options={
                'verbose_name': 'interpreter',
                'verbose_name_plural': 'interpreters',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(help_text='The human-readable name of the job', max_length=250, verbose_name='Job Name')),
                ('program', models.TextField(help_text='The actual program to run (starting with a #!)', verbose_name='Job Program')),
                ('status', model_utils.fields.StatusField(choices=[('initial', 'initial'), ('submitted', 'submitted'), ('success', 'success'), ('failure', 'failure')], default='initial', help_text='The current status of the program', max_length=100, no_check_for_status=True, verbose_name='Job Status')),
                ('remote_directory', models.CharField(help_text='The directory on the remote host to store the program', max_length=250, verbose_name='Job Remote Directory')),
                ('remote_filename', models.CharField(help_text='The filename to store the program to (e.g. reduce.py)', max_length=250, verbose_name='Job Remote Filename')),
                ('interpreter', models.ForeignKey(help_text='The interpreter that this job will run on', on_delete=django.db.models.deletion.PROTECT, related_name='jobs', to='django_remote_submission.Interpreter', verbose_name='Job Interpreter')),
                ('owner', models.ForeignKey(help_text='The user that owns this job', on_delete=django.db.models.deletion.PROTECT, related_name='jobs', to=settings.AUTH_USER_MODEL, verbose_name='Job Owner')),
            ],
            options={
                'verbose_name': 'job',
                'verbose_name_plural': 'jobs',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, help_text='The time this log was created', verbose_name='Log Time')),
                ('content', models.TextField(help_text='The content of this log message', verbose_name='Log Content')),
                ('stream', models.CharField(choices=[('stdout', 'stdout'), ('stderr', 'stderr')], default='stdout', help_text='Output communication channels. Either stdout or stderr.', max_length=6, verbose_name='Standard Stream')),
                ('job', models.ForeignKey(help_text='The job this log came from', on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='django_remote_submission.Job', verbose_name='Log Job')),
            ],
            options={
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('remote_filename', models.TextField(help_text='The filename on the remote server for this result, relative to the remote directory of the job', max_length=250, verbose_name='Remote Filename')),
                ('local_file', models.FileField(help_text='The filename on the local server for this result', max_length=250, upload_to=django_remote_submission.models.job_result_path, verbose_name='Local Filename')),
                ('job', models.ForeignKey(help_text='The job this result came from', on_delete=django.db.models.deletion.CASCADE, related_name='results', to='django_remote_submission.Job', verbose_name='Result Job')),
            ],
            options={
                'verbose_name': 'result',
                'verbose_name_plural': 'results',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(help_text='The human-readable name of the server', max_length=100, verbose_name='Server Name')),
                ('hostname', models.CharField(help_text='The hostname used to connect to the server', max_length=100, verbose_name='Server Hostname')),
                ('port', models.IntegerField(default=22, help_text='The port to connect to for SSH (usually 22)', verbose_name='Server Port')),
                ('interpreters', models.ManyToManyField(to='django_remote_submission.Interpreter', verbose_name='List of interpreters available for this Server')),
            ],
            options={
                'verbose_name': 'server',
                'verbose_name_plural': 'servers',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='server',
            field=models.ForeignKey(help_text='The server that this job will run on', on_delete=django.db.models.deletion.PROTECT, related_name='jobs', to='django_remote_submission.Server', verbose_name='Job Server'),
        ),
    ]