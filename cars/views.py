from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm
from django.views import View
from django.views.generic import ListView, CreateView,DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

""" class CarsView(View):  #metodo da classe View do Django (desativado)
    def get(self, request):
        cars = Car.objects.all().order_by('model') #busca todo objetos da classe carro
        search = search = request.GET.get('search')#variavel que vai receber o valor do campo de busca

        if search:#se houver busca
            cars = cars.filter(model__icontains=search) #busca pelo valor do campo de busca

        return render(request,
            'cars.html',
            {'cars': cars }
        )
        """ 
        
class CarsListView(ListView): #herdando a classe listView
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    
    def get_queryset(self):
        cars = super().get_queryset().order_by('brand__name','model') #ordenação o __ serve para acessar o atributo de outra tabela
        search = self.request.GET.get('search') #filtro
        if search:#se houver busca
            cars = cars.filter(model__icontains=search) #busca pelo valor do campo de busca
        return cars
        
   
@method_decorator(login_required(login_url='login'), name='dispatch')# verifica se o usuario esta logado antes de permitir acesso a view
class NewCarView(CreateView):
    model = Car
    template_name = 'new_car.html'
    form_class = CarModelForm
    success_url = '/cars/'
   
   
class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    
@method_decorator(login_required(login_url='login'), name='dispatch')    
class CarUpdateView(UpdateView):	
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
   
    
    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'