from django.contrib import messages
from django.shortcuts import render


def test(request):
    messages.add_message(request, messages.SUCCESS, 'Hello world.')
    return render(
        request,
        "test.html",
        {}
    )
