from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrencyField(models.PositiveIntegerField):
    description = _(
        "Champ pour sauvegarder de l'argent en centimes (int) dans la base de données, mais récupérer en flottant")

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        return int(round(value * 100))

    def to_python(self, value):
        if value is None or isinstance(value, float):
            return value
        try:
            return float(value) / 100
        except (TypeError, ValueError):
            raise ValidationError(
                _("La valeur doit être un entier or une chaîne de caractères représentant un entier"))

    def from_db_value_to_python(self, value, expression, connection, context):
        return self.to_python(value)
