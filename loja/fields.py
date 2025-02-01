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
