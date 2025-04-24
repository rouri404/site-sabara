from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

def validate_cpf(value):
    cpf = ''.join(filter(str.isdigit, value))
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')
    if len(set(cpf)) == 1:
        raise ValidationError('CPF inválido (todos os dígitos iguais).')
    
    total = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder = (total * 10) % 11
    if remainder == 10 or remainder == 11:
        remainder = 0
    if remainder != int(cpf[9]):
        raise ValidationError('CPF inválido (primeiro dígito verificador incorreto).')
    
    total = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder = (total * 10) % 11
    if remainder == 10 or remainder == 11:
        remainder = 0
    if remainder != int(cpf[10]):
        raise ValidationError('CPF inválido (segundo dígito verificador incorreto).')

def validate_telefone(value):
    digits = ''.join(filter(str.isdigit, value))
    if len(digits) not in (10, 11):
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos (DDD + número).')

def validate_idade(data_nascimento):
    today = date.today()
    age = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
    if age > 18:
        raise ValidationError('Paciente deve ter até 18 anos.')

class Paciente(models.Model):
    TIPO_ATENDIMENTO_CHOICES = [
        ('emergencia', 'Emergência'),
        ('consulta', 'Consulta'),
        ('internacao', 'Internação'),
        ('cirurgia', 'Cirurgia'),
        ('exame', 'Exame'),
        ('vacinacao', 'Vacinação'),
    ]

    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    data_nascimento = models.DateField(validators=[validate_idade])
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    endereco_rua = models.CharField(max_length=200, verbose_name='Rua', default='Rua Desconhecida')
    endereco_numero = models.CharField(max_length=10, blank=True, verbose_name='Número')
    endereco_complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    endereco_bairro = models.CharField(max_length=100, verbose_name='Bairro', default='Desconhecido')
    endereco_cidade = models.CharField(max_length=100, verbose_name='Cidade', default='Cidade Desconhecida')
    endereco_estado = models.CharField(max_length=2, verbose_name='Estado', default='SP')
    telefone = models.CharField(max_length=15, validators=[validate_telefone])
    email = models.EmailField(blank=True, null=True)
    tipo_atendimento = models.CharField(max_length=50, choices=TIPO_ATENDIMENTO_CHOICES)
    plano_saude = models.CharField(max_length=50, blank=True)  # Adicionado para compatibilidade com CSV
    condicao_medica = models.CharField(max_length=100, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    def clean(self):
        if self.cpf:
            cpf_digits = ''.join(filter(str.isdigit, self.cpf))
            if len(cpf_digits) == 11:
                self.cpf = f'{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}'
            else:
                raise ValidationError('CPF deve ter 11 dígitos.')
        if self.telefone:
            digits = ''.join(filter(str.isdigit, self.telefone))
            if len(digits) in (10, 11):
                ddd = digits[:2]
                number = digits[2:]
                if len(number) == 8:
                    self.telefone = f'({ddd}) {number[:4]}-{number[4:]}'
                else:
                    self.telefone = f'({ddd}) {number[:5]}-{number[5:]}'
        super().clean()

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'