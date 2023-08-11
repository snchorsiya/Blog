from django.urls import path, reverse_lazy
from . import views
from .feeds import LatestPostsFeed
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', login_required(auth_views.PasswordChangeView.as_view(template_name='blog/password_change_form.html',success_url=reverse_lazy('blog:change-password-done'))), name='change-password'),
    path('change-password/done/', login_required(auth_views.PasswordChangeDoneView.as_view(template_name = 'blog/password_change_done.html')), name='change-password-done'),
    
    
    path("reset-password/", auth_views.PasswordResetView.as_view(template_name='blog/password_reset_form.html',html_email_template_name='blog/password_reset_email.html'), name="reset_password"),
    path("reset-password/done/", auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name="password_reset_done"),
    path("reset-password-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset-password/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),name='password_reset_complete'),

    path('postlist/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('addpost/', views.add_post, name='add_post'),
   

]
