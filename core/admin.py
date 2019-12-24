from django.contrib import admin

from core.models import User, Repo, Doc, Note

admin.site.register(User)
admin.site.register(Repo)
admin.site.register(Doc)
admin.site.register(Note)
