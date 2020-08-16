from django.contrib.auth.models import User
import django_filters
from .models import Course,Category

class CourseFilter(django_filters.FilterSet):
    # hire_date       = django_filters.DateFilter(field_name='hire_date', lookup_expr='gt')
    title__icontains    = django_filters.CharFilter(label="Judul",field_name='title', lookup_expr='icontains')
    category            = django_filters.ModelMultipleChoiceFilter(field_name='category__id',to_field_name='id',queryset=Category.objects.all())
    price__gte          = django_filters.NumberFilter(field_name='price',lookup_expr='gte')
    price__lte          = django_filters.NumberFilter(field_name='price',lookup_expr='lte')
    start_at__gt        = django_filters.DateFilter(field_name='start_at', lookup_expr='gt')
    start_at__lt        = django_filters.DateFilter(field_name='start_at', lookup_expr='lt')
    # pricee              = django_filters.CharFilter(field_name='title')
    order_by           = django_filters.OrderingFilter(
        fields=(
            ('start_at', 'start_at'),
            # ('title', 'title'),
            ('price', 'price'),
        ),
        choices=(
            ('price', 'Termurah'),
            ('-price', 'Termahal'),
            ('start_at', 'Waktu Terdekat'),
            ('-start_at', 'Waktu Terjauh'),
        ),
    )

    class Meta:
        model = Course
        fields = ['title','price']
        
    