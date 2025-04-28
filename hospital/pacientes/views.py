from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm
import pandas as pd
import plotly.express as px
import requests

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
                print(f"Exceção ao salvar: {str(e)}")
        else:
            print("Erros do formulário:", form.errors)
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{form.fields[field].label}: {error}")
            for error in form.non_field_errors():
                error_messages.append(f"Erro geral: {error}")
            messages.error(request, f'Erro ao cadastrar paciente: {"; ".join(error_messages)}')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/cadastrar.html', {'form': form})

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Paciente atualizado com sucesso!')
                return redirect('listar_pacientes')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar paciente: {str(e)}')
                print(f"Exceção ao atualizar: {str(e)}")
        else:
            print("Erros do formulário:", form.errors)
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{form.fields[field].label}: {error}")
            for error in form.non_field_errors():
                error_messages.append(f"Erro geral: {error}")
            messages.error(request, f'Erro ao atualizar paciente: {"; ".join(error_messages)}')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/editar.html', {'form': form, 'paciente': paciente})

def excluir_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.delete()
            messages.success(request, 'Paciente excluído com sucesso!')
            return redirect('listar_pacientes')
        except Exception as e:
            messages.error(request, f'Erro ao excluir paciente: {str(e)}')
            print(f"Exceção ao excluir: {str(e)}")
    return render(request, 'pacientes/confirmar_exclusao.html', {'paciente': paciente})

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

def analise_dados(request):
    pacientes = Paciente.objects.all().values()
    df = pd.DataFrame(pacientes)
    
    graficos = {}
    if not df.empty:
        # Idade
        df['idade'] = (pd.to_datetime('today') - pd.to_datetime(df['data_nascimento'])).dt.days // 365
        fig_idade = px.histogram(
            df, x='idade', nbins=20, title='Distribuição de Idade dos Pacientes',
            labels={'idade': 'Idade (anos)', 'count': 'Número de Pacientes'},
            color_discrete_sequence=['#0161a4']
        )
        graficos['idade'] = fig_idade.to_html(full_html=False)

        # Tipo de Atendimento
        fig_atendimento = px.pie(
            df, names='tipo_atendimento', title='Distribuição por Tipo de Atendimento',
            labels={'tipo_atendimento': 'Tipo de Atendimento'},
            color_discrete_sequence=['#0161a4', '#7fb538', '#ea0129', '#1e90ff', '#ff4500', '#32cd32']
        )
        graficos['atendimento'] = fig_atendimento.to_html(full_html=False)

        # Sexo
        fig_sexo = px.histogram(
            df, x='sexo', title='Distribuição por Sexo',
            labels={'sexo': 'Sexo', 'count': 'Número de Pacientes'},
            color_discrete_sequence=['#7fb538']
        )
        graficos['sexo'] = fig_sexo.to_html(full_html=False)

        # Cadastros por Data
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro']).dt.date
        cadastros_por_data = df.groupby('data_cadastro').size().reset_index(name='count')
        fig_cadastros = px.line(
            cadastros_por_data, x='data_cadastro', y='count', title='Cadastros de Pacientes por Data',
            labels={'data_cadastro': 'Data de Cadastro', 'count': 'Número de Cadastros'},
            color_discrete_sequence=['#ea0129']
        )
        graficos['cadastros'] = fig_cadastros.to_html(full_html=False)
    else:
        graficos = {
            'idade': "<p>Nenhum dado disponível para idade.</p>",
            'atendimento': "<p>Nenhum dado disponível para tipo de atendimento.</p>",
            'sexo': "<p>Nenhum dado disponível para sexo.</p>",
            'cadastros': "<p>Nenhum dado disponível para cadastros.</p>",
        }
    
    return render(request, 'pacientes/analise.html', {'graficos': graficos})

def sincronizar_iot(request):
    # Lista todos os pacientes
    pacientes = Paciente.objects.all()

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        numero_sala = request.POST.get('numero_sala')

        # Validações
        if not paciente_id or not numero_sala:
            messages.error(request, 'Por favor, selecione um paciente e informe o número da sala.')
            return render(request, 'pacientes/iot.html', {'pacientes': pacientes})

        try:
            numero_sala = int(numero_sala)
            if numero_sala < 1 or numero_sala > 100:
                messages.error(request, 'O número da sala deve estar entre 1 e 100.')
                return render(request, 'pacientes/iot.html', {'pacientes': pacientes})
        except ValueError:
            messages.error(request, 'O número da sala deve ser um valor numérico.')
            return render(request, 'pacientes/iot.html', {'pacientes': pacientes})

        # Obtém o paciente selecionado
        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            messages.error(request, 'Paciente não encontrado.')
            return render(request, 'pacientes/iot.html', {'pacientes': pacientes})

        # Formata a mensagem
        texto = f"{paciente.nome} SALA:{numero_sala}"

        # Envia para o Orion Context Broker
        URL_PATCH = "http://20.197.240.85:1026/v2/entities/Display001/attrs"
        headers = {
            "Content-Type": "application/json",
            "Fiware-Service": "default",
            "Fiware-ServicePath": "/"
        }
        payload = {
            "text": {
                "value": texto,
                "type": "String"
            }
        }
        
        try:
            response = requests.patch(URL_PATCH, json=payload, headers=headers)
            if response.status_code == 204:
                messages.success(request, f"Texto enviado com sucesso: {texto}")
            else:
                messages.error(request, f"Erro ao enviar texto: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Erro na requisição: {str(e)}')
            print(f"Exceção na requisição ao Orion: {str(e)}")

        return redirect('sincronizar_iot')

    return render(request, 'pacientes/iot.html', {'pacientes': pacientes})