import os
import uuid

from django.db import models


class Conditions(models.TextChoices):

    SECOND_HAND = "SH", "Second hand"

    NEW = "N", "New"

    REFURBISHED = "RB", "Refurbished"


class Envios(models.IntegerChoices):
    DHL = 1, "DHL"

    HERMES = 2, "Hermes envio"

    DPD = 3, "DPD"

    GLS = 4, "GLS"

    UPS = 5, "UPS"

    TNT = 6, "TNT"

    OUTRO = 7, "Outro"


class Ofertas(models.IntegerChoices):
    FIXO = 1, "Preço fixo"

    VB = 2, "Base para negociação"

    SD = 3, "Sob demanda"

    PRESENTE = 4, "Para dar de presente"


class AccountType(models.IntegerChoices):
    IS = 1, "Industrial supplier"
    PP = 2, "Private provider"


class CompanySize(models.IntegerChoices):
    SBO = 1, "Small business owner"

    E = 2, "Entrepreneur (with VAT)"


def gerar_nome_aleatorio(instance, filename):
    ext = filename.split(
        '.')[-1]
    novo_nome = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads/', novo_nome)
