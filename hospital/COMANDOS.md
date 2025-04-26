Código pra abrir o servidor Django: 
```bash 
python3 manage.py runserver
```

---

Certificar se as migrações estão aplicadas:
```bash 
python manage.py makemigrations
python manage.py migrate
```

---

Configurar o código pela venv: 

- Criar ambiente virtual: 
```bash
python3 -m venv venv
```

- Acessar o ambiente virtual (de preferência executar tudo por ele): 
```bash
source venv/bin/activate
```

---

Banco de dados:

- Gerar pacientes fictícios (ambiente para testes): 
```bash 
python manage.py shell
>>> from pacientes.models import Paciente
>>> populate_pacientes(100)
```

- Apagar banco de dados:
```bash 
python manage.py shell
>>> from pacientes.models import Paciente
>>> Paciente.objects.all().delete()
```

