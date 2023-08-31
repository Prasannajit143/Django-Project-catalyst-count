import django_filters
from .models import YourModel

class YourModelFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(lookup_expr='icontains')
    industry = django_filters.CharFilter(lookup_expr='icontains')
    year_founded = django_filters.NumberFilter(lookup_expr='exact')
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')
    employee = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = YourModel
        fields = []
