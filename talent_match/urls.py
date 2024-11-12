"""
URL configuration for talent_match project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from talent import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_company/', views.register_company, name='register_company'),
    path('register_user/', views.register_user, name='register_user'),

    path('user_index/', views.user_index, name='user_index'),
    path('company_index/', views.company_index, name='company_index'),
    path('view_jobs/', views.view_jobs, name='view_jobs'),
    path('post_job/', views.post_job, name='post_job'),
    path('company_jobs/', views.company_jobs, name='company_jobs'),

    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('show_job/<int:job_id>/', views.show_job, name='show_job'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
