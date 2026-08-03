from django.shortcuts import render


def index_predicciones(request):
    return render(
        request,
        'predicciones/index_predicciones.html'
    )