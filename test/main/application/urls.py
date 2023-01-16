from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.PostList.as_view(),name="index"),
    path("account/",views.account,name="account"),
    path("login/",views.signin,name="login"),
    path("logout/",views.signout,name="logout"),
    path("contact/",views.contact,name="contact"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_done", auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path("password_reset_confirm/<slug:uidb64>/<slug:token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset_complete", auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path("about_us/", views.about_us, name="About_Us")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
