import random
from datetime import datetime, timedelta
from faker import Faker
from django.utils import timezone
from pacientes.models import Paciente

# Configurar Faker para português brasileiro
fake = Faker('pt_BR')

# Lista de estados brasileiros
ESTADOS = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
    'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
    'SP', 'SE', 'TO'
]

# Lista de tipos de atendimento
TIPOS_ATENDIMENTO = [
    'emergencia', 'consulta', 'internacao', 'cirurgia', 'exame', 'vacinacao'
]

# Lista de condições médicas fictícias
CONDICOES_MEDICAS = [
    'Asma', 'Rinite Alérgica', 'Bronquite', 'Gastrite', 'Dermatite', 'Febre',
    'Infecção Urinária', 'Conjuntivite', '', ''  # Adiciona vazio para maior realismo
]

# Lista de planos de saúde fictícios
PLANOS_SAUDE = [
    'Amil', 'Unimed', 'SulAmérica', 'Bradesco Saúde', 'Porto Seguro', '', ''
]

# Função para gerar CPF válido
def gerar_cpf_valido():
    def calcular_digito(cpf, peso_inicial):
        soma = sum(int(d) * peso for d, peso in zip(cpf, range(peso_inicial, 1, -1)))
        resto = (soma * 10) % 11
        return 0 if resto >= 10 else resto

    while True:
        try:
            cpf = [random.randint(0, 9) for _ in range(9)]
            cpf.append(calcular_digito(cpf, 10))
            cpf.append(calcular_digito(cpf, 11))
            cpf_str = ''.join(map(str, cpf))
            if len(set(cpf_str)) > 1:
                return f'{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}'
        except Exception as e:
            print(f"Erro ao gerar CPF: {e}")
            continue

# Função para gerar pacientes fictícios
def populate_pacientes(n=200):
    pacientes = []
    cpfs_gerados = set(Paciente.objects.values_list('cpf', flat=True))  # Carrega CPFs existentes

    for i in range(n):
        try:
            # Garantir CPF único
            while True:
                cpf = gerar_cpf_valido()
                if cpf not in cpfs_gerados:
                    cpfs_gerados.add(cpf)
                    break

            # Gerar data de nascimento (pacientes com até 18 anos)
            data_nascimento = fake.date_between(start_date='-18y', end_date='today')

            # Gerar telefone (10 ou 11 dígitos)
            # Escolher aleatoriamente entre 10 ou 11 dígitos
            num_digitos = random.choice([10, 11])
            ddd = str(random.randint(11, 99))  # DDD válido (11 a 99)
            if num_digitos == 11:
                numero = ''.join([str(random.randint(0, 9)) for _ in range(9)])
                telefone = f'({ddd}) {numero[:5]}-{numero[5:]}'
            else:
                numero = ''.join([str(random.randint(0, 9)) for _ in range(8)])
                telefone = f'({ddd}) {numero[:4]}-{numero[4:]}'

            paciente = Paciente(
                nome=fake.name(),
                cpf=cpf,
                data_nascimento=data_nascimento,
                sexo=random.choice(['M', 'F', 'O']),
                endereco_rua=fake.street_name(),
                endereco_numero=str(random.randint(1, 9999)),
                endereco_complemento=fake.secondary_address() if random.choice([True, False]) else '',
                endereco_bairro=fake.bairro(),
                endereco_cidade=fake.city(),
                endereco_estado=random.choice(ESTADOS),
                telefone=telefone,
                email=fake.email() if random.choice([True, False]) else None,
                tipo_atendimento=random.choice(TIPOS_ATENDIMENTO),
                plano_saude=random.choice(PLANOS_SAUDE),
                condicao_medica=random.choice(CONDICOES_MEDICAS),
                observacoes=fake.text(max_nb_chars=200) if random.choice([True, False]) else '',
                data_cadastro=timezone.now() - timedelta(days=random.randint(0, 365))
            )
            pacientes.append(paciente)
        except Exception as e:
            print(f"Erro ao criar paciente {i+1}: {e}")
            continue

    # Inserir pacientes no banco de dados
    try:
        Paciente.objects.bulk_create(pacientes, ignore_conflicts=True)
        print(f"{len(pacientes)} pacientes criados com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir pacientes: {str(e)}")

if __name__ == "__main__":
    populate_pacientes(200)