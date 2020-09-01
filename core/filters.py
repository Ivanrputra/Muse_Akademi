from django.contrib.auth.models import User
import django_filters
from .models import Course,Category,MentorData,Order
from django.db.models import Q
from distutils.util import strtobool
from django.utils.translation import gettext_lazy as _
from django_select2.forms import (
    HeavySelect2MultipleWidget,
    HeavySelect2Widget,
    ModelSelect2MultipleWidget,
    ModelSelect2TagWidget,
    ModelSelect2Widget,
    Select2MultipleWidget,
    Select2Widget,
)


COURSE_STATUS_CHOICE = (
    ('1', _('Publish')),
    ('0', _('Tidak Publish')),
)


class CourseFilter(django_filters.FilterSet):
    # hire_date       = django_filters.DateFilter(field_name='hire_date', lookup_expr='gt')
    title__icontains    = django_filters.CharFilter(method='filter_title__icontains')
    # title__icontains    = django_filters.CharFilter(label="Judul",field_name='title', lookup_expr='icontains')
    # status              = django_filters.ChoiceFilter(choices=MentorData.MentorStatus.choices,empty_label="-Pilih Status-")
    status              = django_filters.ChoiceFilter(field_name='is_publish',choices=COURSE_STATUS_CHOICE,empty_label="-Pilih Status Publish-")
    category            = django_filters.ModelMultipleChoiceFilter(widget=Select2MultipleWidget(attrs={'style':'width:100%','data-placeholder':'  Cari dan pilih macam kategori untuk kursus yang anda buat'}),
    field_name='category__id',to_field_name='id',queryset=Category.objects.all())
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
        empty_label="-Pilih Urutan-"
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
    status                  = django_filters.ChoiceFilter(choices=MentorData.MentorStatus.choices,empty_label="-Pilih Status-")
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
        empty_label="-Pilih Urutan-"
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
    invoice_no__icontains       = django_filters.CharFilter(label="Invoice",field_name='invoice_no', lookup_expr='icontains')
    status                      = django_filters.ChoiceFilter(choices=Order.OrderStatusManagement.choices+Order.OrderStatusUser.choices,
                                    empty_label="-Pilih Status-")
    class Meta:
        model = Order
        fields = ['invoice_no','course','price','user']
    