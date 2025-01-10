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

### `loja/anuncio/{id}`

##### Trás um anúncio pelo seu id

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

### `loja/anuncio/subcategoria/{nome_subcategoria}`

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

### `loja/anuncio/categoria/{nome_categoria}`

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