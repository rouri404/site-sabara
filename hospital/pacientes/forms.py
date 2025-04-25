from django import forms
from .models import Paciente
from django.core.validators import EmailValidator

# Lista de estados brasileiros
ESTADOS_BRASILEIROS = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]

class PacienteForm(forms.ModelForm):
    endereco_estado = forms.ChoiceField(
        choices=ESTADOS_BRASILEIROS,
        widget=forms.Select(attrs={'class': 'estado-select'}),
        label='Estado'
    )

    class Meta:
        model = Paciente
        fields = [
            'nome', 'cpf', 'data_nascimento', 'sexo', 'endereco_rua', 'endereco_numero',
            'endereco_complemento', 'endereco_bairro', 'endereco_cidade', 'endereco_estado',
            'telefone', 'email', 'tipo_atendimento', 'condicao_medica', 'observacoes'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-input', 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '(XX) XXXXX-XXXX'}),
            'tipo_atendimento': forms.Select(),
        }
        labels = {
            'cpf': 'CPF',
            'endereco_rua': 'Rua',
            'endereco_numero': 'Número',
            'endereco_complemento': 'Complemento',
            'endereco_bairro': 'Bairro',
            'endereco_cidade': 'Cidade',
            'endereco_estado': 'Estado',
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf_digits = ''.join(filter(str.isdigit, cpf))
            if len(cpf_digits) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
            return f'{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}'
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            digits = ''.join(filter(str.isdigit, telefone))
            if len(digits) not in (10, 11):
                raise forms.ValidationError('Telefone deve ter 10 ou 11 dígitos (DDD + número).')
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator(message='Digite um email válido.')
            validator(email)
        return email