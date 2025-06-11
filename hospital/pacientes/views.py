from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    pacientes_list = Paciente.objects.all().order_by('-data_cadastro')
    paginator = Paginator(pacientes_list, 15)  # Mostra 15 pacientes por página

    page = request.GET.get('page')
    try:
        pacientes = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página.
        pacientes = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (ex: 9999), exibe a última página de resultados.
        pacientes = paginator.page(paginator.num_pages)

    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

def analise_dados(request):
    pacientes = Paciente.objects.all().values()
    df = pd.DataFrame(pacientes)
    
    graficos = {}
    estatisticas = {}
    
    if not df.empty:
        # Cálculo de Idade
        df['idade'] = (pd.to_datetime('today') - pd.to_datetime(df['data_nascimento'])).dt.days // 365
        
        # Estatísticas Gerais
        estatisticas['total_pacientes'] = len(df)
        estatisticas['media_idade'] = round(df['idade'].mean(), 1)
        
        # Faixa Etária dos Pacientes
        fig_idade = px.histogram(
            df, x='idade', nbins=20, 
            title='Faixa Etária dos Pacientes',
            labels={'idade': 'Idade (anos)', 'count': 'Número de Pacientes'},
            color_discrete_sequence=['#0161a4'],
            template='plotly_white'
        )
        fig_idade.update_layout(
            bargap=0.1,
            xaxis_title="Idade (anos)",
            yaxis_title="Número de Pacientes",
            title_font_size=18,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        graficos['faixa_etaria'] = fig_idade.to_html(full_html=False, div_id="grafico-faixa-etaria")

        # Tipos de Atendimento
        df['tipo_atendimento'] = df['tipo_atendimento'].str.title()  # Capitaliza os valores
        fig_atendimento = px.pie(
            df, names='tipo_atendimento', 
            title='Tipos de Atendimento',
            labels={'tipo_atendimento': 'Tipo de Atendimento'},
            color_discrete_sequence=['#0161a4', '#7fb538', '#ea0129', '#1e90ff', '#ff4500', '#32cd32'],
            template='plotly_white'
        )
        fig_atendimento.update_traces(textinfo='percent+label', textposition='inside')
        fig_atendimento.update_layout(
            title_font_size=18,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        graficos['tipos_atendimento'] = fig_atendimento.to_html(full_html=False, div_id="grafico-tipos-atendimento")

        # Distribuição por Gênero
        df['sexo'] = df['sexo'].replace({'M': 'Masculino', 'F': 'Feminino'})
        fig_sexo = px.histogram(
            df, x='sexo', 
            title='Distribuição por Gênero',
            labels={'sexo': 'Gênero', 'count': 'Número de Pacientes'},
            color_discrete_sequence=['#7fb538'],
            template='plotly_white'
        )
        fig_sexo.update_layout(
            xaxis_title="Gênero",
            yaxis_title="Número de Pacientes",
            title_font_size=18,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        graficos['genero'] = fig_sexo.to_html(full_html=False, div_id="grafico-genero")

        # Pacientes com Observações Adicionais
        df['tem_observacoes'] = df['observacoes'].notnull() & (df['observacoes'] != '')
        df['tem_observacoes'] = df['tem_observacoes'].map({True: 'Com Observações', False: 'Sem Observações'})
        estatisticas['percent_observacoes'] = round((df['tem_observacoes'] == 'Com Observações').mean() * 100, 1)
        fig_observacoes = px.pie(
            df, names='tem_observacoes', 
            title='Pacientes com Observações Adicionais',
            labels={'tem_observacoes': 'Status de Observações'},
            color_discrete_sequence=['#ff4500', '#32cd32'],
            template='plotly_white'
        )
        fig_observacoes.update_traces(textinfo='percent+label', textposition='inside')
        fig_observacoes.update_layout(
            title_font_size=18,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        graficos['observacoes'] = fig_observacoes.to_html(full_html=False, div_id="grafico-observacoes")
    else:
        estatisticas = {
            'total_pacientes': 0,
            'media_idade': 0,
            'percent_observacoes': 0
        }
        graficos = {
            'faixa_etaria': "<p class='text-gray-500'>Nenhum dado disponível para faixa etária.</p>",
            'tipos_atendimento': "<p class='text-gray-500'>Nenhum dado disponível para tipos de atendimento.</p>",
            'genero': "<p class='text-gray-500'>Nenhum dado disponível para gênero.</p>",
            'observacoes': "<p class='text-gray-500'>Nenhum dado disponível para observações adicionais.</p>",
        }
    
    return render(request, 'pacientes/analise.html', {
        'graficos': graficos,
        'estatisticas': estatisticas
    })

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