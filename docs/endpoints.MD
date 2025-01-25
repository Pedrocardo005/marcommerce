# Documentação relativa aos endpoints da aplicação

### `loja/cat-subcat/`
##### Trazer categorias e subcategorias.

GET
```json
[
    {
        "nome": "categoria 1",
        "sub_categorias": [
            {
                "nome": "subcategoria 1"
            },
            {
                "nome": "subcategoria 2"
            },
            {
                "nome": "subcategoria 3"
            }
        ]
    },
    {
        "nome": "categoria 2",
        "sub_categorias": [
            {
                "nome": "subcategoria 4"
            },
            {
                "nome": "subcategoria 5"
            },
            {
                "nome": "subcategoria 6"
            }
        ]
    }
]
```

Necessário passar o idioma.
Retornar no máximo 3 subcategorias de cada categoria.

### `loja/categorias/`

##### Trás todas as categorias

GET
```json
[
    {
        "nome": "categoria 1"
    },
    {
        "nome": "categoria 2"
    }
]
```

Necessita passar o idioma também.

### `loja/listsearch?q=&city=`

##### Trás anúncios pelo nome da categoria e pela cidade e código postal

GET
```json
[
    {
        "id": 1,
        "nome": "produto 1",
        "preco": 11.08,
        "descricao": "descricao qualquer",
        "condicao": "condição do item"
    }
]
```

### `loja/anuncios/{id}`

##### (GET) Trás um anúncio pelo seu id

GET
```json
{
    "nome": "nome posto no anúncio",
    "valor": 10.95,
    "views": 5,
    "data_publicacao": "13/12/2024",
    "id_anunciante": 1,
    "email_anunciante": "abc@gmail.com"
}
```

##### (PUT) Edita um anúncio

PUT
```json
{
    "id": 1,
    "id_categoria": 1,
    "vendendo": true,
    "titulo": "Fiat Palio",
    "descricao": "Carro seminovo em perfeito estado, 10.000km rodados",
    "tipo_oferta": 1,
    "preco": 40000.00,
    "fotos": [
        {
            "imagem1": "imagem em um formato lá para envio",
            "ordem": 3
        }
    ],
    "condicao": "Usado",
    "envio": 2,
    "pagamento_paypal": true,
    "codigo_postal": "40000-000",
    "cidade": "São Paulo",
    "rua": "Rua São Marcelo",
    "numero": 12,
    "provedor": "Casas Bahia",
    "telefone": "71984287792"
}
```

##### (DELETE) Remove um anúncio

Remove um registro de anúncio. Mas somente se for o criador do anúncio.

DELETE
```json
{
    "id": 1,
}
```

### `loja/anuncios/subcategoria/{nome_subcategoria}`

##### Trás anúncios pela subcategoria

GET
```json
[
    {
        "id": 1,
        "nome": "produto 1",
        "preco": 11.08,
        "descricao": "descricao qualquer",
        "condicao": "condição do item"
    },
    {
        "id": 2,
        "nome": "produto 2",
        "preco": 11.08,
        "descricao": "descricao qualquer dois",
        "condicao": "condição do item dois"
    }
]
```

### `loja/anuncios/categoria/{nome_categoria}`

##### Trás anúncios pela categoria

GET
```json
[
    {
        "id": 1,
        "nome": "produto 1",
        "preco": 11.08,
        "descricao": "descricao qualquer",
        "condicao": "condição do item"
    },
    {
        "id": 2,
        "nome": "produto 2",
        "preco": 11.08,
        "descricao": "descricao qualquer dois",
        "condicao": "condição do item dois"
    }
]
```

### `loja/login`

##### Faz login no site

POST
```json
{
    "email": "teste@gmail.com",
    "senha": "12345678"
}
```
retorno
```json
{
    "token": "aofnaoisfjaiosfnaksn9au1jrf-0a"
}
```

### `loja/logout`

##### Faz logout no site

POST
```json
{
    "token": "aofnaoisfjaiosfnaksn9au1jrf-0a"
}
```

Obs: Não precisa nem passar nada, irá automaticamente deslogar o usuário

### `loja/register`

##### Registra usuário no sistema

POST
```json
{
    "email": "nada@gmail.com",
    "password": "abcdefg",
    "repeat_password": "abcdefg",
    "username": "Marinho",
    "type": "privado"
}
```

ou

```json
{
    "email": "nada@gmail.com",
    "password": "abcdefg",
    "repeat_password": "abcdefg",
    "username": "Marinho",
    "type": "comercial"
}
```

### `loja/anuncios/usuario/{id_usuario}`

##### Trás anúncios pelo usuário

GET
```json
[
    {
        "id": 1,
        "ativo": true,
        "views": 10,
        "data_expirar": "25/12/2025",
        "preco": 10.9,
        "url_imagem": "https://aws.s3.com.br/09u1rnknfas9f0"
    }
]
```

Precisa estar autenticado
Provavelmente retornará apenas se for vendedor
Provavelmente nem precisará do id do usuário porque o servidor consegue saber.

### `loja/anuncios`

##### Cria um anúncio

POST
```json
{
    "id_categoria": 1,
    "vendendo": true,
    "titulo": "Fiat Palio",
    "descricao": "Carro seminovo em perfeito estado, 10.000km rodados",
    "tipo_oferta": 1,
    "preco": 40000.00,
    "fotos": [
        {
            "imagem1": "imagem em um formato lá para envio",
            "ordem": 3
        }
    ],
    "condicao": "Usado",
    "envio": 2,
    "pagamento_paypal": true,
    "codigo_postal": "40000-000",
    "cidade": "São Paulo",
    "rua": "Rua São Marcelo",
    "numero": 12,
    "provedor": "Casas Bahia",
    "telefone": "71984287792"
}
```

### `loja/anuncios/change_status/{id_anuncio}`

##### (PATCH) Desativa ou ativa anuncio

O usuário deve ser o criador do anúncio

PATCH
```json
{
    "id": 1,
    "vendendo": false,
}
```

retorno

```json
{
    "id_categoria": 1,
    "vendendo": false,
    "titulo": "Fiat Palio",
    "descricao": "Carro seminovo em perfeito estado, 10.000km rodados",
    "tipo_oferta": 1,
    "preco": 40000.00,
    "fotos": [
        {
            "imagem1": "imagem em um formato lá para envio",
            "ordem": 3
        }
    ],
    "condicao": "Usado",
    "envio": 2,
    "pagamento_paypal": true,
    "codigo_postal": "40000-000",
    "cidade": "São Paulo",
    "rua": "Rua São Marcelo",
    "numero": 12,
    "provedor": "Casas Bahia",
    "telefone": "71984287792"
}
```

### `loja/anuncios/favorite`

##### (POST) Favorita anuncio

POST
```json
{
    "id_usuario": 1,
    "id_anuncio": 1
}
```

##### (DELETE) Remove anúncio dos favoritos

DELETE
```json
{
    "id_usuario": 1,
    "id_anuncio": 1
}
```

### `loja/anuncios/ofertados`

##### (GET) Traz anuncios que tiveram ofertas

GET
```json
[
    {
        "id": 1,
        "valor": 1500.00,
        "mensagem": "Interesse na sua oferta",
        "anuncio": {
            "id": 1,
            "titulo": "Produto ofertado",
            "preco": 10.5,
            "views": 200
        }
    }
]
```

### `loja/anuncios/ofertar`

##### (POST) Faz oferta pelo anúncio

POST
```json
{
    "id_anuncio": 1,
    "valor": 1500.00,
    "mensagem": "Mensagem indicando interesse no produto"
}
```

### `loja/ofertas/aceitar`

##### (POST) Aceita oferta pelo anúncio

POST
```json
{
    "id": 1,
    "valor": 1500.00
}
```

### `loja/usuarios/alterar_foto`

##### (PATCH) Altera foto do usuário

PATCH
```json
{
    "id_usuario": 1,
    "foto_usuario": "BYTE"
}
```
