# Documentação relativa aos endpoints da aplicação

### `api/cat-subcat/`
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

### `api/categorias/`

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

##### Trás anúncios pelo nome, pela cidade e código postal

GET
```json
[
    {
        "id": 1,
        "titulo": "produto 1",
        "preco": 11.08,
        "descricao": "descricao qualquer",
        "condicao": "condição do item"
    }
]
```

O parâmetro `q` é o nome do anuncio, `city` é o nome da cidade ou código postal.

### `api/anuncios/{id}`

##### (GET) Trás um anúncio pelo seu id

GET
```json
{
    "titulo": "nome posto no anúncio",
    "preco": 10.95,
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

### `api/anuncios/edit/{id_anuncio}`

##### (GET) Trás o anúncio com as suas informações editáveis

GET

retorno
```json
{
    "categoria_name": "Lições e educação",
    "sub_categoria_name": "Mais",
    "tipo_oferta": 1,
    "titulo": "Titulo qualquer",
    "vendendo": true,
    "preco": 10000,
    "photos": [
        {
            "ordem": 1,
            "url_imagem": "http://link.com.br/foto1"
        },
        {
            "ordem": 2,
            "url_imagem": "http://link.com.br/foto2"
        }
    ],
    "condicao": "SH",
    "envio": 1,
    "custo_envio": 50.00,
    "pagamento_paypal": true,
    "codigo_postal": "40000000",
    "cidade": "Salvador",
    "rua": "Rua A",
    "numero": 14,
    "provedor": "Baianão",
    "telefone": "7199999999"
}
```

### `api/anuncios/subcategoria/{id_subcategoria}`

##### Trás anúncios pela subcategoria

GET
```json
[
    {
        "id": 1,
        "titulo": "produto 1",
        "preco": 11.08,
        "descricao": "descricao qualquer",
        "condicao": "condição do item"
    },
    {
        "id": 2,
        "titulo": "produto 2",
        "preco": 11.08,
        "descricao": "descricao qualquer dois",
        "condicao": "condição do item dois"
    }
]
```

### `api/anuncios/categoria/{id_categoria}`

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

### `api/login`

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

### `api/logout`

##### Faz logout no site

POST
```json
{
    "token": "aofnaoisfjaiosfnaksn9au1jrf-0a"
}
```

Obs: Não precisa nem passar nada, irá automaticamente deslogar o usuário

### `api/register`

##### Registra usuário no sistema

POST
```json
{
    "email": "nada@gmail.com",
    "password": "abcdefg",
    "username": "Marinho",
    "account_type": 2
}
```

ou

```json
{
    "email": "nada@gmail.com",
    "password": "abcdefg",
    "username": "Marinho",
    "account_type": 1
}
```

### `api/anuncios/usuario/{id_usuario}`

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

### `api/anuncios`

##### Cria um anúncio

POST
```json
{
    "sub_categoria_id": 1,
    "data_expirar": "24/10/2100",
    "ativo": true,
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
    "condicao": "SH",
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

### `api/anuncios/change_status/{id_anuncio}`

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

### `api/anuncios/favorite`

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

### `api/anuncios/ofertados`

##### (GET) Traz anuncios que tiveram ofertas

Só traz a última mensagem.
Endpoint para a página `/messenger`

GET
```json
[
    {
        "id": 1,
        "valor": 1500.00,
        "data_hora": "24/10/2024 12:00",
        "mensagem": "Interesse na sua oferta",
        "vendido": false,
        "chat_room": "11_10",
        "anuncio": {
            "id": 1,
            "titulo": "Produto ofertado",
            "preco": 10.5,
            "views": 200
        }
    }
]
```

### `api/anuncios/ofertados/{id_anuncio}`

Traz as mensagens daquela oferta (chat de conversa).
Trazer ordenado do mais velho para o mais novo como última mensagem.

GET
```json
[
    {
        "id": 1,
        "remetente": "José",
        "data_hora": "24/10/2024 12:00",
        "mensagem": "teste 123"
    }
]
```

### `api/anuncios/ofertar`

##### (POST) Faz oferta pelo anúncio

POST
```json
{
    "id_anuncio": 1,
    "valor": 1500.00,
    "mensagem": "Mensagem indicando interesse no produto"
}
```

### `api/ofertas/aceitar`

##### (POST) Aceita oferta pelo anúncio

POST
```json
{
    "id_anuncio": 1,
    "id_oferta": 1
}
```

### `api/usuarios/alterar_foto`

##### (PATCH) Altera foto do usuário

PATCH
```json
{
    "id_usuario": 1,
    "foto_usuario": "BYTE"
}
```

### `api/usuarios/editar_usuario`

##### (PUT) Edita informações do usuário

```json
{
    "id": 1,
    "email": "teste@gmail.com",
    "account_type": 1,
    "company_size": 1,
    "company_name": "texto qualquer",
    "first_name": "Primeiro nome",
    "last_name": "Ultimo nome",
    "street": "Rua a",
    "street_number": 14,
    "postcode": "40350-570",
    "city": "São Paulo",
    "commercial_provider": "Texto longo qualquer",
    "right_withdrawal": "Texto longo qualquer",
    "conditions": "Texto longo qualquer",
    "protection_notice": "Texto longo qualquer",
    "legal_notice": "Texto longo qualquer"
}
```

### `api/usuarios/alterar_senha`

##### (PATCH) Altera senha do usuário

PATCH
```json
{
    "id": 1,
    "old_password": "aslkfmmaksf",
    "new_password": "12345678",
    "repeat_password": "12345678"
}
```

### `api/usuarios/resetar_senha`

##### (POST) Reseta senha do usuário

POST
```json
{
    "email": "exemplo@gmail.com"
}
```

### `api/usuarios/confirm_resetar_senha`

##### (POST) Cria uma nova senha para o usuário

POST
```json
{
    "uid": "uid-from-url",
    "token": "token-from-url",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```
