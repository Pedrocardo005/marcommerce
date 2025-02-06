from rest_framework import serializers

from loja.models import Categoria, SubCategoria


class SubCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoria
        fields = ['nome']


class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = SubCategoriaSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ['nome', 'subcategorias']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not self.context.get('show_subcategorias', True):
            representation.pop('subcategorias', None)

        return representation
