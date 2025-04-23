from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm
import pandas as pd
import plotly.express as px
from django.http import HttpResponse

def home(request):
    return render(request, 'pacientes/home.html')

def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Paciente cadastrado com sucesso!')
                return redirect('listar_pacientes')
            except Exception as e:
                messages.error(request, f'Erro ao salvar paciente: {str(e)}')
        else:
            # Exibir erros detalhados do formulário
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, f'Erro ao cadastrar paciente: {"; ".join(error_messages)}')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/cadastrar.html', {'form': form})

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

def analise_dados(request):
    pacientes = Paciente.objects.all().values()
    df = pd.DataFrame(pacientes)
    
    if not df.empty:
        df['idade'] = (pd.to_datetime('today') - pd.to_datetime(df['data_nascimento'])).dt.days // 365
        fig_idade = px.histogram(df, x='idade', nbins=20, title='Distribuição de Pacientes por Idade')
        grafico_idade = fig_idade.to_html(full_html=False)
        fig_atendimento = px.pie(df, names='tipo_atendimento', title='Tipos de Atendimento')
        grafico_atendimento = fig_atendimento.to_html(full_html=False)
    else:
        grafico_idade = "<p>Nenhum dado disponível.</p>"
        grafico_atendimento = "<p>Nenhum dado disponível.</p>"
    
    return render(request, 'pacientes/analise.html', {
        'grafico_idade': grafico_idade,
        'grafico_atendimento': grafico_atendimento,
    })