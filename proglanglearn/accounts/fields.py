# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class StringListField(models.TextField):
#     description = _(
#         "Un champ pour enregistrer une liste en tant que chaîne de caractères")

#     def get_db_prep_value(self, value, *args, **kwargs):
#         if value is None:
#             return None
#         return ';'.join([str(val) for val in value])

#     def to_python(self, value):
#         if value is None or not isinstance(value, str):
#             return []
#         return value.split(';')

#     def from_db_value(self, value, expression, connection, context):
#         return self.to_python(value)
