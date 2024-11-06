from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from .models import Car, CarInvetory
from django.db.models import Sum
from openai_api.client import get_car_ai_bio


def car_inventory_update():
    cars_count = Car.objects.all().count() #conta quantos carros existem
    cars_value = Car.objects.aggregate( #realiza uma consulta no banco de dados
        total_value = Sum('value') #soma o valor de todos os carros
    ) ['total_value'] #retorna o valor da soma
    CarInvetory.objects.create( #cria um novo registro na model CarInvetory com os valores levantados na consulta acima
        cars_count=cars_count,
        cars_value=cars_value
    )
    
@receiver(post_save, sender=Car) #acompnhar evento de salva registro na model Car
def car_post_save(sender, instance, **kwargs):
    car_inventory_update()
    
    
@receiver(post_delete, sender=Car) #marca a função para acompnhar evento na model Car
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()
    
    
@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        ai_bio = get_car_ai_bio(
            instance.model, instance.brand, instance.model_year
        )
        instance.bio = ai_bio
        
    if not instance.photo:
        instance.photo = "cars/sem_imagem.png"