import os
import django
import pandas as pd
from datetime import datetime

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

# Importar o modelo Paciente
from pacientes.models import Paciente

# Caminho do arquivo CSV
csv_path = '/home/gabriel-couto/Área de trabalho/site-sabara/hospital/pacientes.csv'

# Ler o CSV
df = pd.read_csv(csv_path)

# Importar pacientes
for _, row in df.iterrows():
    paciente = Paciente(
        cpf=row['cpf'],
        nome=row['nome'],
        data_nascimento=datetime.strptime(row['data_nascimento'], '%Y-%m-%d').date(),
        sexo=row['sexo'],
        endereco_rua=row['endereco_rua'],
        endereco_numero=row['endereco_numero'],
        endereco_complemento=row['endereco_complemento'],
        endereco_bairro=row['endereco_bairro'],
        endereco_cidade=row['endereco_cidade'],
        endereco_estado=row['endereco_estado'],
        telefone=row['telefone'],
        email=row['email'] if pd.notnull(row['email']) and row['email'] != '' else None,
        tipo_atendimento=row['tipo_atendimento'],
        plano_saude=row['plano_saude'],
        condicao_medica=row['condicao_medica'],
        observacoes=row['observacoes']
    )
    paciente.full_clean()  # Aplicar validações do modelo
    paciente.save()

print(f"{len(df)} pacientes importados com sucesso!")