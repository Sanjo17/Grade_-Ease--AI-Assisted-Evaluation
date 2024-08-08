# Generated by Django 3.0.5 on 2024-03-24 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0007_auto_20240317_1901'),
        ('student', '0002_remove_student_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_file', models.FileField(upload_to='answers/student_answer')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_file', models.FileField(upload_to='answers/answer_key')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Course')),
            ],
        ),
    ]