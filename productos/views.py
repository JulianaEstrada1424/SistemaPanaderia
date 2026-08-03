from django.shortcuts import render


def inicio(request):
    return render(request, "productos/inicio.html")