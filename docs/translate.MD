# Traduções com o django

Foi utilizado o seguinte tutorial para realizar as traduções:
https://testdriven.io/blog/multiple-languages-in-django/

### Como criar traduções

{% trans "Coloque aqui o que deseja traduzir" %}

Ou pode utilizar os blocos de tradução:

```django
{% blocktrans %}{% endblocktrans %}
```

Rode o seguinte comando para criar as versões de tradução
```shell
django-admin makemessages --all --ignore=env
```

Traduza as mensagens

Depois compile as traduções
```shell
django-admin compilemessages --ignore=env
```

### Deploy com o heroku

Comando para adicionar os pacotes do gettext ao projeto
```bash
heroku buildpacks:add https://github.com/grauwoelfchen/heroku-buildpack-gettext
```

Depois de ter dado o comando, faça uma alteração no projeto e dê um commit:
```bash
git push heroku main
```