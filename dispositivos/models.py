from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    consumo = models.IntegerField()
    estado = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Medicion(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    consumo = models.IntegerField()

    def __str__(self):
        return f"{self.dispositivo} - {self.consumo}W"


class Alerta(models.Model):
    mensaje = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50)
    medicion = models.ForeignKey(Medicion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alerta: {self.mensaje}"


class DispositivoAlerta(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    fecha_generada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dispositivo} - {self.alerta}"
