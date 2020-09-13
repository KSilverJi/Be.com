from django.contrib import admin
from mate.models import Mate, MatePhoto, MateQuest, MateMsg
#mate=post, matephoto=Photo

# MatePhoto 클래스를 inline으로 나타낸다.
class MatePhotoInline(admin.TabularInline):
    model = MatePhoto

# Mate 클래스는 해당하는 MatePhoto 객체를 리스트로 관리한다.
class MateAdmin(admin.ModelAdmin):
    inlines = [MatePhotoInline, ]

admin.site.register(Mate, MateAdmin)
admin.site.register(MateQuest)
admin.site.register(MateMsg)
#admin.site.register(Task)
