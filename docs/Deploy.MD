# DEPLOY Heroku

### Faça o login no Heroku
```bash
heroku login
```

 Depois, irá abrir uma página no browser para efetuar o login.

 Logo depois disso, estará pronto para rodar o comando para fazer o push:
```bash
git push heroku main
```

### Criar um super user

 Comando heroku run roda os comandos no servidor, como mostrado a seguir:
```bash
heroku run python3 manage.py createsuperuser
```
