from django.db import models
from github3.client import User as GUser
from github3.client import Client
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

class GithubUser(models.Model):
    login = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True,null=True)
    public_repo_count = models.PositiveSmallIntegerField(default=0)

    
    

    class Meta:
        ordering = ('login',)
        db_table = 'github_user'

    def __unicode__(self):
        return self.login
    
    @property
    def user_client(self):
        return GUser(Client())


    def get_absolute_url(self):
        return 'http://github.com/%s' % (self.login)

    def save(self, *args, **kwargs):
        if not self.id:
            self.fetch_github()
        super(GithubUser, self).save(*args, **kwargs)
   
    
    def fetch_github(self):
        user = self.user_client.user_info(self.login)
        if user:
            self.name = user.get('name','')
            self.email = user.get('email','')
            self.public_repo_count = int(user.get('public_repos',0))
        return user

    def fetch_repos(self):
        repos = self.user_client.user_repos(self.login)
        if repos:
            for repo in repos:
                project, created = Project.objects.get_or_create(
                        user=self, github_repo=repo.get('name',''))
                project.title = repo.get('name','')
                project.description = repo.get('description','')
                project.save()
        return repos
    
    @property
    def repos(self):
        self.fetch_repos()
        return Project.objects.filter(user=self)
    


    


class Project(models.Model):
    user = models.ForeignKey(GithubUser, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    github_repo = models.CharField(max_length=255)

    
    class Meta:
        ordering = ('title',)
        unique_together = ('user', 'slug')
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)
   
 
    def get_absolute_url(self):
        return reverse('github_project_detail', args=[self.slug])
   
    
    @property
    def github_url(self):
        return 'http://github.com/%s/%s' % (self.user.login, self.github_repo)
    

    
