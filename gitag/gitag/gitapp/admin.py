from django.contrib import admin
from gitapp.models import GithubUser
from gitapp.models import Project 



class GithubUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'name')
    search_fields = ('login', 'name')

    actions = ['fetch_github', 'fetch_repos']

    def fetch_github(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_github():
                user.save()
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_github.short_description = 'Fetch from Github'

    def fetch_repos(self, request, queryset):
        updated = []
        for user in queryset:
            if user.fetch_repos():
                updated.append(user.login)
        self.message_user(request, '%s successfully updated.' % ', '.join(updated))
    fetch_repos.short_description = 'Fetch repos from Github'
    
    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description',)
    prepopulated_fields = {"slug": ("title",)}
    

admin.site.register(GithubUser, GithubUserAdmin)
admin.site.register(Project, ProjectAdmin)
