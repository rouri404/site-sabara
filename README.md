<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=yellow" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-5.2.1-green?logo=django" alt="Django"/>
  <img src="https://img.shields.io/badge/Fiware-IoT-orange?logo=fiware" alt="Fiware"/>
  <img src="https://img.shields.io/badge/TailwindCSS-Styling-38B2AC?logo=tailwind-css" alt="TailwindCSS"/>
  <img src="https://img.shields.io/badge/Plotly-Graphs-3F4F75?logo=plotly" alt="Plotly"/>
</p>

<h1 align="center">🏥 Sabará Hospital Infantil - Sistema de Gerenciamento de Pacientes</h1>
<p align="center">Um sistema de cadastro simples de pacientes e eficiente, desenvolvido em Django/Python.</p>

---

🌟 **Bem-vindo ao Sistema de Gerenciamento de Pacientes do Sabará Hospital Infantil!** 🌟  
Este é um projeto apaixonante que combina tecnologia e cuidado, criado para facilitar o dia a dia de um hospital pediátrico. Nosso objetivo? Simplificar o cadastro, gerenciamento e análise de dados de pacientes, trazendo amor e tecnologia para a saúde das crianças! 💙

### 👥 Membros do Grupo:
- [Ana Luiza](https://github.com/anarand) -
  <a href="https://www.linkedin.com/in/ana-luiza-santana-124023240/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
  </a>
- [Gabriel Couto](https://github.com/rouri404) -
  <a href="https://www.linkedin.com/in/gabricouto/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="linkedin-icon">
  </a>
- [Gabriel Kato](https://github.com/kato8088) -
  <a href="https://www.linkedin.com/in/gabrikato/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="linkedin-icon">
  </a>
- [João Vitor](https://github.com/joaomatosq) -
  <a href="https://www.linkedin.com/in/joaomatosq/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="linkedin-icon">
  </a>

## 🎯 Sobre o Projeto

O **Sabará Hospital Infantil** é referência no cuidado pediátrico, e este sistema foi desenvolvido para ajudar na gestão de pacientes com até 18 anos. Com uma interface intuitiva e cheia de recursos, ele permite cadastrar pacientes, editar registros, visualizar dados em gráficos interativos, sincronizar dados com dispositivos IoT, e muito mais. Tudo isso com um design moderno e responsivo, perfeito para médicos, enfermeiros e administradores.

🚀 **Por que este projeto é especial?**  
- Ele foi pensado para o público pediátrico, garantindo que apenas pacientes com até 18 anos sejam cadastrados.  
- Oferece gráficos interativos para insights rápidos sobre os dados dos pacientes.  
- Permite integração com dispositivos IoT para exibir informações em displays remotos.  
- Tem validações rigorosas (como CPF e telefone) para garantir a qualidade dos dados.  

## ✨ Funcionalidades

Aqui estão os principais recursos do sistema, projetados para facilitar a vida de quem cuida das crianças:

- **📝 Cadastro de Pacientes**:
  - Formulário detalhado com campos validados (CPF, telefone, email, idade).  
  - Máscaras automáticas para CPF (`XXX.XXX.XXX-XX`) e telefone (`(XX) XXXXX-XXXX`).  
  - Seleção de estados brasileiros com uma lista pronta (de Acre a Tocantins 🇧🇷).  
- **📋 Listagem de Pacientes**:
  - Veja todos os pacientes em uma tabela organizada.  
  - Opções para editar ou excluir registros com um clique.  
- **✍️ Edição e Exclusão**:
  - Edite informações de pacientes com facilidade.  
  - Confirmação antes de excluir para evitar acidentes.  
- **📊 Análise de Dados**:
  - Gráficos interativos com Plotly:  
    - Distribuição de idade dos pacientes (em histogramas).  
    - Tipos de atendimento (em gráficos de pizza coloridos 🥧).  
    - Distribuição por sexo.  
    - Cadastros ao longo do tempo (em gráficos de linha 📈).  
- **🌐 Sincronização IoT**:
  - Envie informações de pacientes (nome e sala) para displays remotos conectados via ESP32.  
  - Integração com Orion Context Broker para comunicação em tempo real.  
  - Formato da mensagem: `'nome do paciente' SALA:'número da sala'` (ex.: "João Silva SALA:42").  
- **📱 Interface Responsiva**:
  - Navegação perfeita em desktops e dispositivos móveis.  
  - Menu mobile com ícones intuitivos (🏠 Home, ➕ Cadastrar, 📜 Listar, 📊 Análise, 🌐 Sincronização IoT).  
- **💬 Feedback ao Usuário**:
  - Mensagens de sucesso (em verde ✅) ou erro (em vermelho 🚨) com animações suaves.

## 🌟 Diferenciais

O que torna este sistema único? Aqui estão alguns destaques:  
- **Validação Avançada** 🔍:  
  - CPF com verificação de dígitos verificadores (nada de CPFs inválidos aqui!).  
  - Restrição de idade para pacientes pediátricos (≤ 18 anos).  
  - Telefone validado para 10 ou 11 dígitos.  
- **Design Encantador** 🎨:  
  - Interface estilizada com Tailwind CSS, fontes suaves (Poppins) e ícones do FontAwesome.  
  - Animações sutis, como `fadeIn` e efeitos de hover, para uma experiência visual incrível.  
- **Análise Visual** 📊:  
  - Gráficos interativos que ajudam a entender os dados dos pacientes de forma rápida e clara.  
- **Integração IoT** 🌐:  
  - Comunicação com dispositivos IoT para exibir informações em tempo real em displays remotos.  
- **Testes Facilitados** 🛠️:  
  - Um script personalizado (`populate_pacientes.py`) para gerar 200 pacientes fictícios com dados realistas, perfeito para testes.

## 🛠️ Tecnologias Utilizadas

Aqui está o arsenal tecnológico que dá vida ao projeto:

| **Categoria**       | **Tecnologias**                     |
|---------------------|-------------------------------------|
| **Backend**         | Django (Python) + SQLite 🐍         |
| **Frontend**        | HTML5, Tailwind CSS, FontAwesome, Google Fonts (Poppins) 🎨 |
| **Interatividade**  | JavaScript (máscaras de entrada, menu mobile) 📱 |
| **Análise de Dados**| `pandas` + `plotly.express` 📈      |
| **Integração IoT**  | `requests` + Orion Context Broker 🌐 |
| **Dados Fictícios** | `faker` para geração de dados realistas 🌟 |

## 🚀 Como Começar?

Siga estas etapas para colocar o sistema no ar e começar a gerenciar pacientes!

### Pré-requisitos
- 🐍 Python 3.8 ou superior
- Virtualenv (recomendado para isolar dependências)
- SQLite (padrão, mas você pode usar PostgreSQL ou MySQL se preferir)

### Instalação

1. **Clone o repositório** 📥:
   ```bash
   git clone https://github.com/rouri404/site-sabara.git
   cd hospital
   ```

2. **Crie e ative um ambiente virtual** 🛡️:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências** 📦:
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o banco de dados** 🗃️:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **(Opcional) Crie um superusuário para o Django Admin** 👤:
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor** 🌐:
   ```bash
   python manage.py runserver
   ```
   Acesse o sistema em `http://127.0.0.1:8000/`. 🎉

## 🖥️ Como Usar?

Explore as funcionalidades do sistema com facilidade:

- **🏠 Página Inicial**: `http://127.0.0.1:8000/`  
  Uma tela acolhedora para começar sua jornada.  
- **➕ Cadastrar Paciente**: `http://127.0.0.1:8000/cadastrar/`  
  Preencha o formulário com os dados do paciente (nome, CPF, telefone, etc.).  
- **📜 Listar Pacientes**: `http://127.0.0.1:8000/listar/`  
  Veja todos os pacientes cadastrados e edite/exclua se precisar.  
- **📊 Análise de Dados**: `http://127.0.0.1:8000/analise/`  
  Visualize gráficos incríveis para entender os dados dos pacientes.  
- **🌐 Sincronização IoT**: `http://127.0.0.1:8000/sincronizar-iot/`  
  Selecione um paciente e uma sala (1 a 100) para enviar ao display conectado via ESP32.  
- **🔐 Django Admin**: `http://127.0.0.1:8000/admin/`  
  Gerencie os dados com o superusuário criado.

### 🌟 Dica: Gere Dados Fictícios para Testes
Quer testar o sistema com dados realistas? Popule o banco com 200 pacientes fictícios!  
1. Certifique-se de que o `faker` está instalado:
   ```bash
   pip install faker
   ```
2. Use o para gerar pacientes:
   ```bash
   python manage.py shell
   >>> from pacientes.populate_pacientes import populate_pacientes
   >>> populate_pacientes(200)
   ```

### 🧹 Limpar o Banco de Dados
1. Para remover todos os pacientes e começar de novo:
   ```bash 
   python manage.py shell
   >>> from pacientes.models import Paciente
   >>> Paciente.objects.all().delete()
   ```

## 💡 Diferenciais Técnicos

- **Validação de CPF** ✅: Implementação detalhada para verificar dígitos, garantindo apenas CPFs válidos.  
- **Responsividade** 📱: Interface que funciona perfeitamente em desktops e dispositivos móveis.  
- **Animações Suaves** ✨: Efeitos visuais como `fadeIn` e hover para uma experiência encantadora.  
- **Gráficos Interativos** 📈: Use Plotly para explorar dados de forma visual e dinâmica.  
- **Integração IoT** 🌐: Comunicação com Orion Context Broker para exibir dados em displays conectados via ESP32.

💙 **Sabará Hospital Infantil** - Cuidando com amor e tecnologia da saúde das crianças! 💙
