# Generated by Django 5.2 on 2025-04-23 22:23

import pacientes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paciente",
            name="cpf",
            field=models.CharField(
                max_length=14, unique=True, validators=[pacientes.models.validate_cpf]
            ),
        ),
    ]
