from django.shortcuts import render

def inicio(request):
    return render(request, "inicio.html")

def panel_dispositivos(request):
    dispositivos = [
        {"nombre": "Sensor Temperatura", "consumo": 50},
        {"nombre": "Medidor Solar", "consumo": 120},
        {"nombre": "Sensor Movimiento", "consumo": 30},
        {"nombre": "Calefactor", "consumo": 200},
    ]

    consumo_maximo = 100
    # Contar cuántos dispositivos superan el consumo máximo
    criticos = sum(1 for d in dispositivos if d["consumo"] > consumo_maximo)

    return render(request, "dispositivos/panel.html", {
        "dispositivos": dispositivos,
        "consumo_maximo": consumo_maximo,
        "criticos": criticos
    })
