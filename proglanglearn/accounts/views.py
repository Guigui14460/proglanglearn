from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'accounts/index.html', context)


def contact(request):
    return render(request, 'accounts/contact.html')


def terms(request):
    return render(request, 'accounts/terms.html')


def about(request):
    return render(request, 'accounts/about.html')


def privacy(request):
    return render(request, 'accounts/privacy.html')


def error_403(request, exception):
    return render(request, '403.html', {})


def error_404(request, exception):
    return render(request, '404.html', {})


def error_500(request):
    return render(request, '500.html', {})
