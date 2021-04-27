import django_filters
from .models import Exhibition, Category
from django_filters import CharFilter, NumberFilter, ModelChoiceFilter


def categories(request):
    return Category.objects.all()


class ExhibitionFilter(django_filters.FilterSet):
    lastName = CharFilter(field_name='student__last_name', lookup_expr='icontains')
    firstName = CharFilter(field_name='student__first_name', lookup_expr='icontains')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    categories = ModelChoiceFilter(queryset=categories)
    startDate_year__gt = NumberFilter(field_name='startDate', lookup_expr='year__gt')
    startDate_year__lt = NumberFilter(field_name='startDate', lookup_expr='year__lt')

    class Meta:
        model = Exhibition
        fields = ['title', 'categories']