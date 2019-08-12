from io import BytesIO
import random
import string

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import gettext as _

import xhtml2pdf.pisa as pisa

from .models import Coupon


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        if coupon.limited == 0 or coupon.deactivate_date < timezone.now():
            return None
    except ObjectDoesNotExist:
        return None
    return coupon


class RenderPDF:
    @staticmethod
    def render(path: str, params: dict, file_name: str):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf')
            # response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
            response['Content-Disposition'] = f'inline; filename="{file_name}.pdf"'
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)
