from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .models import Library

def user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user:login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_mentor and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def mentor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user:login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_mentor and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user:login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

import functools
def is_student_have(arg1):
    def decorator(function):
        @login_required
        @functools.wraps(function)
        def wrap(request,*args, **kwargs):
            have = False
            print(arg1)
            print(kwargs)
            if arg1 == 'Library':
                if 'pk' in kwargs           : have = Library.objects.filter(pk=kwargs['pk'],user=request.user).exists()
                elif 'course_pk' in kwargs  : have = Library.objects.filter(course__pk=kwargs['course_pk'],user=request.user).exists()
            elif arg1 == 'Session': 
                if 'pk' in kwargs           : have = Library.objects.filter(course__session=kwargs['pk'],user=request.user).exists()
            elif arg1 == 'Exam':
                if 'pk' in kwargs           : have = Library.objects.filter(course__exam=kwargs['pk'],user=request.user).exists()
            elif arg1 == 'ExamAnswer':
                if 'pk' in kwargs           : have = Library.objects.filter(course__exam__examanswer=kwargs['pk'],user=request.user).exists()
                elif 'exam_pk' in kwargs    : have = Library.objects.filter(course__exam=kwargs['exam_pk'],user=request.user).exists()
            elif arg1 == 'ExamProject':
                if 'pk' in kwargs           : have = Library.objects.filter(course__exam__examanswer__examproject=kwargs['pk'],user=request.user).exists()
                elif 'exam_pk' in kwargs    : have = Library.objects.filter(course__exam=kwargs['exam_pk'],user=request.user).exists()
            
            if have : 
                return function(request, *args, **kwargs)
            else    : 
                # raise Http404
                raise PermissionDenied  
        return wrap
    return decorator