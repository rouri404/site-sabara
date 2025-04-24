import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar Faker para português do Brasil
fake = Faker('pt_BR')

# Função para gerar CPF válido
def gerar_cpf():
    def calcular_digito(cpf, pesos):
        soma = sum(int(d) * p for d, p in zip(cpf, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    cpf = [str(random.randint(0, 9)) for _ in range(9)]
    cpf.append(calcular_digito(cpf, [10, 9, 8, 7, 6, 5, 4, 3, 2]))
    cpf.append(calcular_digito(cpf, [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]))
    return ''.join(cpf)

# Gerar 100 pacientes
pacientes = []
tipos_atendimento = ['emergencia', 'consulta', 'internacao', 'cirurgia', 'exame', 'vacinacao']
sexos = ['M', 'F', 'O']
planos_saude = ['Amil', 'Bradesco Saúde', 'SulAmérica', 'Unimed', '']
condicoes_medicas = ['Asma', 'Diabetes', 'Alergia', 'Nenhuma', '']
estados = ['SP', 'RJ', 'MG', 'PR']

for _ in range(100):
    # Data de nascimento: crianças de 1 a 18 anos
    data_nasc = fake.date_of_birth(minimum_age=1, maximum_age=18)
    
    # Gerar telefone com 10 ou 11 dígitos
    ddd = random.choice(['11', '21', '31', '41'])
    if random.choice([True, False]):
        numero = ''.join([str(random.randint(0, 9)) for _ in range(9)])  # 11 dígitos
        telefone = f'{ddd}{numero}'
    else:
        numero = ''.join([str(random.randint(0, 9)) for _ in range(8)])  # 10 dígitos
        telefone = f'{ddd}{numero}'
    
    paciente = {
        'cpf': gerar_cpf(),  # Será formatado no modelo
        'nome': fake.name(),
        'data_nascimento': data_nasc.strftime('%Y-%m-%d'),
        'sexo': random.choice(sexos),
        'endereco_rua': fake.street_name(),
        'endereco_numero': str(random.randint(1, 9999)),
        'endereco_complemento': fake.secondary_address() if random.choice([True, False]) else '',
        'endereco_bairro': fake.bairro(),
        'endereco_cidade': fake.city(),
        'endereco_estado': random.choice(estados),
        'telefone': telefone,
        'email': fake.email() if random.choice([True, False]) else '',
        'tipo_atendimento': random.choice(tipos_atendimento),
        'plano_saude': random.choice(planos_saude),
        'condicao_medica': random.choice(condicoes_medicas),
        'observacoes': fake.text(max_nb_chars=200) if random.choice([True, False]) else ''
    }
    pacientes.append(paciente)

# Criar DataFrame e salvar como CSV
df = pd.DataFrame(pacientes)
csv_path = '/home/gabriel-couto/Área de trabalho/site-sabara/hospital/pacientes.csv'
df.to_csv(csv_path, index=False, encoding='utf-8')
print(f"Arquivo CSV gerado em: {csv_path}")