from django.contrib import admin
from base.models import Question, Player, Reply


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'statement', 'enable')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('answered_at', 'player', 'question', 'score')
