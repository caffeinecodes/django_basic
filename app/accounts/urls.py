from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'app.accounts.views',
    url(r'^register/$','register'),
    url(r'^login/$','login'),
    url(r'^accounts/create_user/$','create_user'),
    url(r'^accounts/login_user/$','login_user'),
    url(r'^confirm-email/(?P<key>.*)/$', 'confirm_email'),
    url(r'^reset-password/$', 'reset_password'),
    url(r'^forgot-password/$', 'forgot_password'),
    url(r'^update_password/(?P<key>.*)/$','update_new_password'),
    url(r'^reset_password/$','update_password_new'),
    url(r'^verify-email/$', 'verify_email'),
    url(r'^email-verified/$', 'email_verified'),
    url(r'^send-verification-email/$', 'send_verification_email'),

)
