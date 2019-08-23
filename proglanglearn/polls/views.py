from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView

from main.mixins import NavbarSearchMixin
from .models import Poll, Item, Vote
from .utils import set_cookie


class VoteView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            poll = get_object_or_404(Poll, pk=kwargs.get('poll_pk'))
            item = get_object_or_404(Item, pk=request.GET.get('item', None))
            Vote.objects.create(
                poll=poll, ip=request.META['REMOTE_ADDR'], user=request.user, item=item)

            response = HttpResponse(status=200)
            set_cookie(response, poll.get_cookie_name(), kwargs.get('poll_pk'))

            context = {'poll': poll, 'items': Item.objects.filter(poll=poll)}
            html = render_to_string(
                'polls/includes/ajax_result.html', context, request=request)
            return JsonResponse({'html': html})
        return HttpResponse(status=400)


class PollDetailView(NavbarSearchMixin, View):
    template_name = "polls/poll_detail.html"

    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs.get('poll_pk'))
        if Vote.objects.filter(poll=poll, ip=request.META['REMOTE_ADDR']).exists():
            messages.warning(request, _("Vous avez déjà répondu à ce sondage"))
            return redirect('polls:poll_result', poll_pk=poll.pk)
        context = super().get_context_data(**kwargs)
        context['poll'] = poll
        context['items'] = Item.objects.filter(poll=poll)
        return render(request, self.template_name, context)


class PollResultView(NavbarSearchMixin, View):
    template_name = "polls/poll_result.html"

    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs.get('poll_pk'))
        context = super().get_context_data(**kwargs)
        context['poll'] = poll
        context['items'] = Item.objects.filter(poll=poll)
        return render(request, self.template_name, context)


class PollListView(NavbarSearchMixin, ListView):
    paginate_by = 20
    queryset = Poll.objects.all()
