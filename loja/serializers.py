from rest_framework import serializers

from loja.models import Anuncio, Categoria, SubCategoria


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

    id_anunciante = serializers.IntegerField(source="usuario.id", read_only=True)

    email_anunciante = serializers.CharField(source="usuario.email", read_only=True)

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
