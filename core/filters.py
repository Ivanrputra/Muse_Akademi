from django.contrib.auth.models import User
import django_filters
from .models import Course,Category,MentorData,Order
from django.db.models import Q

class CourseFilter(django_filters.FilterSet):
    # hire_date       = django_filters.DateFilter(field_name='hire_date', lookup_expr='gt')
    title__icontains    = django_filters.CharFilter(method='filter_title__icontains')
    # title__icontains    = django_filters.CharFilter(label="Judul",field_name='title', lookup_expr='icontains')
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

    def filter_title__icontains(self, queryset, name, value):
        q = []
        qobjects = Q()
        for query in value.split():
            qobjects |= Q(title__icontains=query)
        return queryset.filter(qobjects)

    class Meta:
        model = Course
        fields = ['title','price']

class MentorDataFilter(django_filters.FilterSet):
    user_email__icontains   = django_filters.CharFilter(method='filter_user_email__icontains')
    order_by                = django_filters.OrderingFilter(
        fields=(
            ('mentor__email', 'email'),
            ('mentor__username', 'username'),
            ('created_at', 'created_at'),
        ),
        choices=(
            ('email', 'Email (Asc)'),
            ('-email', 'Email (Desc)'),
            ('username', 'Username (Asc)'),
            ('-username', 'Username (Desc)'),
            ('created_at', 'Dibuat (Asc)'),
            ('-created_at', 'Dibuat (Desc)'),
        ),
    )

    def filter_user_email__icontains(self, queryset, name, value):
        q = []
        qobjects = Q()
        qobjects |= Q(mentor__email__icontains=value)
        qobjects |= Q(mentor__firstname__icontains=value)
        qobjects |= Q(mentor__lastname__icontains=value)
        qobjects |= Q(mentor__username__icontains=value)
        return queryset.filter(qobjects).distinct()

    class Meta:
        model = MentorData
        fields = ['created_at','mentor',]

class OrderDataFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['invoice_no','course','price','user']
    