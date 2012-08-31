from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to


urlpatterns = patterns('gitapp.views',
    url(r'^$', 
        view='project_list', 
        name='github_project_list'
    ),
 
    (r'^users/$',
        redirect_to,
        {'url': 'home' }
    ),
    url(r'^users/(?P<login>[\w-]+)/$', 
        view='user_detail', 
        name='github_user_detail'
    ),
    url(r'^(?P<project_slug>[\w-]+)/$', 
        view='project_detail', 
        name='github_project_detail'
    ),
    
)
