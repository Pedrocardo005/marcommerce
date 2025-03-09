import json

from rest_framework import serializers

from loja.models import (Anuncio, Categoria, CustomUser, Favorito, FotoAnuncio,
                         SubCategoria)


class SubCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoria
        fields = ["name"]


class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = SubCategoriaSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ["nome", "subcategorias"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not self.context.get("show_subcategorias", True):
            representation.pop("subcategorias", None)

        return representation


class SearchAnuncioSerializer(serializers.ModelSerializer):

    preco = serializers.FloatField()

    class Meta:
        model = Anuncio
        fields = ["id", "titulo", "preco", "descricao", "condicao"]


class GetAnuncioSerializer(serializers.ModelSerializer):

    preco = serializers.FloatField()

    id_anunciante = serializers.IntegerField(
        source="usuario.id", read_only=True)

    email_anunciante = serializers.CharField(
        source="usuario.email", read_only=True)

    class Meta:
        model = Anuncio
        fields = [
            "titulo",
            "preco",
            "views",
            "data_publicacao",
            "id_anunciante",
            "email_anunciante",
        ]


class UpdateAnuncioSerializer(serializers.ModelSerializer):

    preco = serializers.FloatField(read_only=True)

    sub_categoria_id = serializers.IntegerField(source="sub_categoria.id")

    categoria_name = serializers.CharField(
        source="sub_categoria.categoria.nome", read_only=True
    )

    sub_categoria_name = serializers.CharField(
        source="sub_categoria.name", read_only=True
    )

    class Meta:
        model = Anuncio
        fields = [
            "vendendo",
            "titulo",
            "descricao",
            "tipo_oferta",
            "preco",
            "condicao",
            "envio",
            "custo_envio",
            "pagamento_paypal",
            "codigo_postal",
            "cidade",
            "rua",
            "numero",
            "provedor",
            "telefone",
            "sub_categoria_id",
            "categoria_name",
            "sub_categoria_name",
        ]

    def update(self, instance, validated_data):
        sub_categoria = validated_data.pop("sub_categoria")
        instance.sub_categoria_id = sub_categoria.pop("id")
        return super().update(instance, validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'username',
            'account_type'
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AnuncioUsuarioSerializer(serializers.ModelSerializer):
    data_expirar = serializers.SerializerMethodField()

    preco = serializers.FloatField()

    url_foto = serializers.ReadOnlyField()

    class Meta:
        model = Anuncio
        fields = ['id', 'ativo', 'views', 'data_expirar', 'preco', 'url_foto']

    def get_data_expirar(self, obj):
        # Formata a data no formato "dd/mm/aaaa"
        return obj.data_expirar.strftime('%d/%m/%Y')


class CreateFotoAnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoAnuncio
        fields = ['ordem', 'imagem']


class CreateAnuncioSerializer(serializers.ModelSerializer):
    data_expirar = serializers.DateTimeField(
        format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    sub_categoria_id = serializers.IntegerField()
    usuario_id = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)
    fotos = CreateFotoAnuncioSerializer(many=True, required=False)

    class Meta:
        model = Anuncio
        fields = ['id', 'sub_categoria_id', 'usuario_id', 'data_expirar', 'ativo', 'vendendo',
                  'titulo', 'descricao', 'preco', 'tipo_oferta', 'condicao',
                  'envio', 'pagamento_paypal', 'codigo_postal', 'cidade',
                  'rua', 'numero', 'provedor', 'telefone', 'fotos']

    def create(self, validated_data):
        anuncio = super().create(validated_data)
        fotos = self.initial_data.pop('fotos', [])
        for imgs in fotos:
            for foto_data in imgs:
                foto_data['ordem'] = int(foto_data['ordem'][0])
                FotoAnuncio.objects.create(anuncio=anuncio, **foto_data)
        return anuncio


class ChangeStatusAnuncioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Anuncio
        fields = ['id', 'vendendo']


class CreateFavoriteAnuncioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    id_usuario = serializers.IntegerField(source='usuario.pk')
    id_anuncio = serializers.IntegerField(source='anuncio.pk')

    class Meta:
        model = Favorito
        fields = ['id', 'id_usuario', 'id_anuncio']
