from django.db import models
from django.core.exceptions import ValidationError

def validate_cpf(value):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, value))
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')
    
    # Verifica se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        raise ValidationError('CPF inválido (todos os dígitos iguais).')
    
    # Validação dos dígitos verificadores
    def calculate_digit(cpf, length):
        total = sum(int(cpf[i]) * (length - i) for i in range(length))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    digit1 = calculate_digit(cpf, 10)
    digit2 = calculate_digit(cpf, 11)
    if int(cpf[9]) != digit1 or int(cpf[10]) != digit2:
        raise ValidationError('CPF inválido (dígitos verificadores incorretos).')

class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    endereco = models.CharField(max_length=300)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    tipo_atendimento = models.CharField(max_length=50, choices=[
        ('emergencia', 'Emergência'),
        ('consulta', 'Consulta'),
        ('internacao', 'Internação'),
    ])
    condicao_medica = models.CharField(max_length=100, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    def clean(self):
        # Normaliza o CPF para incluir máscara antes de salvar
        if self.cpf:
            cpf_digits = ''.join(filter(str.isdigit, self.cpf))
            if len(cpf_digits) == 11:
                self.cpf = f'{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}'
            else:
                raise ValidationError('CPF deve ter 11 dígitos.')
        super().clean()