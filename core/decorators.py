from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound
from django.urls import reverse,reverse_lazy

from .models import Library,Course,Exam,MitraUser,Mitra

# def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
#     """
#     Decorator for views that checks that the user is logged in, redirecting
#     to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_authenticated,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     print('123')
#     if function:
#         return actual_decorator(function)
#     return actual_decorator

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

            if arg1 == 'Library':
                if 'pk' in kwargs           : have = Library.objects.filter(pk=kwargs['pk'],user=request.user).exists()
                elif 'course_pk' in kwargs  : have = Library.objects.filter(course__pk=kwargs['course_pk'],user=request.user).exists()
                elif 'library_pk' in kwargs : have = Library.objects.filter(pk=kwargs['library_pk'],user=request.user).exists()
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

def is_staff_have(arg1):
    def decorator(function):
        @staff_required
        @functools.wraps(function)
        def wrap(request,*args, **kwargs):
            have = False

            if arg1 == 'Course':
                if 'pk' in kwargs           : have = Course.objects.filter(pk=kwargs['pk'],admin=request.user).exists()
                elif 'course_pk' in kwargs  : have = Course.objects.filter(pk=kwargs['course_pk'],admin=request.user).exists()
            elif arg1 == 'Session':
                if 'pk' in kwargs           : have = Course.objects.filter(session=kwargs['pk'],admin=request.user).exists()
                elif 'course_pk' in kwargs  : have = Course.objects.filter(pk=kwargs['course_pk'],admin=request.user).exists()
            elif arg1 == 'SessionData':
                if 'pk' in kwargs           : have = Course.objects.filter(session__sessiondata=kwargs['pk'],admin=request.user).exists()
                elif 'session_pk' in kwargs : have = Course.objects.filter(session=kwargs['session_pk'],admin=request.user).exists()
            elif arg1 == 'Exam':
                if 'pk' in kwargs           : have = Course.objects.filter(exam=kwargs['pk'],admin=request.user).exists()
                elif 'course_pk' in kwargs  : have = Course.objects.filter(pk=kwargs['course_pk'],admin=request.user).exists()
            elif arg1 == 'ExamAnswer':
                if 'pk' in kwargs           : have = Course.objects.filter(exam__examanswer=kwargs['pk'],admin=request.user).exists()
            elif arg1 == 'Library':
                if 'pk' in kwargs           : have = Course.objects.filter(library=kwargs['pk'],admin=request.user).exists()

            if have : 
                return function(request, *args, **kwargs)
            else    : 
                # raise Http404
                raise PermissionDenied  
        return wrap
    return decorator

def is_mentor_have(arg1):
    def decorator(function):
        @mentor_required
        @functools.wraps(function)
        def wrap(request,*args, **kwargs):
            have = False
            print(arg1)
            print(kwargs)
            if arg1 == 'Course':
                if 'pk' in kwargs               : have = Course.objects.filter(pk=kwargs['pk'],session__mentor=request.user).exists()
            elif arg1 == 'ExamAnswer':
                if 'pk' in kwargs               : have = Course.objects.filter(exam__examanswer=kwargs['pk'],session__mentor=request.user).exists()
            elif arg1 == 'ExamReport':
                if 'pk' in kwargs               : have = Course.objects.filter(exam__examanswer__examreport=kwargs['pk'],session__mentor=request.user).exists()
                elif 'examanswer_pk' in kwargs  : have = Course.objects.filter(exam__examanswer=kwargs['examanswer_pk'],session__mentor=request.user).exists()
            elif arg1 == 'ExamAnswer':
                if 'pk' in kwargs               : have = Course.objects.filter(exam__examanswer=kwargs['pk'],admin=request.user).exists()
            elif arg1 == 'Session': 
                # print()
                # print(Course.objects.filter(session=kwargs['pk'],session__mentor=request.user).exists())
                if 'pk' in kwargs               : have = Course.objects.filter(session=kwargs['pk']).filter(session__mentor=request.user).exists()
            elif arg1 == 'Evaluation':
                if 'pk' in kwargs               : have = Course.objects.filter(library__evaluation=kwargs['pk'],session__mentor=request.user).exists()
                elif 'library_pk' in kwargs     : have = Course.objects.filter(library=kwargs['library_pk'],session__mentor=request.user).exists()
                

            if have : 
                return function(request, *args, **kwargs)
            else    : 
                # raise Http404
                raise PermissionDenied  
        return wrap
    return decorator

def is_user_have_mitra_valid(arg1):
    def decorator(function):
        @mentor_required
        @functools.wraps(function)
        def wrap(request,*args, **kwargs):
            have = False
            if arg1 == 'Mitra':
                if 'pk' in kwargs   : have = MitraUser.objects.filter(mitra=kwargs['pk'],mitra__status="CO",user=request.user).exists()
            
            if have : 
                return function(request, *args, **kwargs)
            else    : 
                # raise Http404
                raise PermissionDenied  
        return wrap
    return decorator

def check_exam_time(arg1):
    def decorator(function):
        @functools.wraps(function)
        def wrap(request,*args, **kwargs):
            exam = None

            if arg1 == 'Exam':
                if 'exam_pk' in kwargs          : exam = get_object_or_404(Exam,pk=kwargs['exam_pk'])
            elif arg1 == 'ExamAnswer':
                if 'pk' in kwargs               : exam = Exam.objects.filter(examanswer=kwargs['pk']).first()
            elif arg1 == 'ExamProject':
                if 'pk' in kwargs               : exam = Exam.objects.filter(examanswer__examproject=kwargs['pk']).first()

            if exam.close_at < timezone.now():
                messages.warning(request,f'Deadline tugas telah berakhir pada waktu : {timezone.localtime(exam.close_at)}')
                return HttpResponseRedirect(reverse_lazy('app:classroom-exams',kwargs={'course_pk':exam.course.id}))
                
            return function(request, *args, **kwargs)
        return wrap
    return decorator



# def check_time(function):
#     def _function(request,*args, **kwargs):
#         classroom = None
#         if 'pk' in kwargs               : classroom = get_object_or_404(models.Classroom,pk=kwargs['pk'])
#         elif 'classroom_pk' in kwargs   : classroom = get_object_or_404(models.Classroom,pk=kwargs['classroom_pk'])
        
#         if classroom:
#             if not classroom.is_publish:
#                 messages.warning(request,str('Classroom is not published'))
#                 return HttpResponseRedirect(reverse_lazy('app:index'))
#             if classroom.closed_at<datetime.date.today():
#                 messages.warning(request,str('Classroom already closed'))
#                 return HttpResponseRedirect(reverse_lazy('app:index'))
#         else:
#             messages.warning(request,str('Classroom not Found'))
#             return HttpResponseRedirect(reverse_lazy('app:index'))

#         return function(request, *args, **kwargs)
#     return _function