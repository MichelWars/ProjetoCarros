from django import forms

from cars.models import Car

# forma complexa de criar um form no django
""" class CarForm(forms.Form):
    model = forms.CharField(max_length=200)
    brand = forms.ModelChoiceField(Brand.objects.all())#da um select na tabela Brande e mostra as opções para selecionar
    factory_year = forms.IntegerField()
    model_year = forms.IntegerField()
    plate = forms.CharField(max_length=10)
    value = forms.FloatField()
    photo = forms.ImageField()

    def save(self):
        car = Car(
            model=self.cleaned_data["model"],
            brand=self.cleaned_data["brand"],
            factory_year=self.cleaned_data["factory_year"],
            model_year=self.cleaned_data["model_year"],
            plate=self.cleaned_data["plate"],
            value=self.cleaned_data["value"],
            photo=self.cleaned_data["photo"],
        )
        car.save()
        return car """


# forma mais simples de criar um form no django
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    # depois é só ir em new_car_view em views.py e alterar a chamada da função para essa.
    def clean_value(
        self,
    ):   # para criar funções de validação deve-se sempre usar o clean_ para que o django entenda que é uma função de validação
        value = self.cleaned_data.get('value')
        if value < 20000:
            self.add_error(
                'value', 'Valor minimo do carro deve ser R$20.000,00'
            )
        return value

    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')
        if factory_year < 1975:
            self.add_error(
                'factory_year', 'Ano de fabricação deve ser maior que 1975'
            )
        return factory_year
