# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from gitapp.models import GithubUser
from gitapp.models import Project 
from django.core.exceptions import ObjectDoesNotExist



def index(request,template_name='gitapp/user_list.html'):
    user_list = GithubUser.objects.all()

    return render_to_response(template_name, 
            { 'user_list': user_list}, 
            context_instance=RequestContext(request))

def project_detail(request,project_slug,template_name='gitapp/project_detail.html'):
    project = get_object_or_404(Project,slug=project_slug)

    return render_to_response(template_name,
            { 'project': project},
            context_instance=RequestContext(request))



def project_list(request,template_name='gitapp/project_list.html'):
    username = request.GET.get('username',None)
    if not username :
        raise Http404
    try: 
        user = GithubUser.objects.get(login=username)
    except ObjectDoesNotExist:
        user = GithubUser.objects.create(login=username)

    fetch_repos = user.fetch_repos()
    project_list = user.repos
    
    return render_to_response(template_name,
            { 'project_list': project_list},
            context_instance=RequestContext(request))





def user_detail(request,login,template_name='gitapp/user_detail.html'):
    user=get_object_or_404(GithubUser,login=login)
    return render_to_response(template_name,
            { 'user': user},
            context_instance=RequestContext(request))



    


