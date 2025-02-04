# MarCommerce

Projeto para criação de um ecommerce de exemplo.

## Ferramentas

Python 3.9.6

Django 4.2.7

Docker

Docker-compose

### Iniciando o projeto

1. Faça o clone do projeto no sua máquina com o comando:
```bash
git clone https://github.com/Pedrocardo005/marcommerce
```

2. Entre na pasta do projeto copiado:
```bash
cd marcommerce
```

3. Rode o banco de dados da aplicação com o docker-compose:
```bash
sudo make only-database
```

4. Crie um ambiente virtual:
```bash
python -m venv env
```

5. Ative o ambiente virtual:
```bash
source env/bin/activate
```

6. Instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

7. Rode a aplicação:
```bash
python manage.py runserver
```

8. Aplique as migrações:
```bash
python manage.py migrate
```
