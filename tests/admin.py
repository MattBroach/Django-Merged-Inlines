from django.contrib import admin

from merged_inlines.admin import MergedInlineAdmin

from .models import Author, Play, Poem, Kingdom, King, Soldier


# Admin classes
class PlayInline(admin.TabularInline):
    model = Play


class PoemInline(admin.TabularInline):
    model = Poem


class AuthorAdmin(MergedInlineAdmin):
    inlines = [PlayInline, PoemInline]


class KingInline(admin.TabularInline):
    model = King


class SoldierInline(admin.TabularInline):
    model = Soldier


class KingdomAdmin(MergedInlineAdmin):
    inlines = [KingInline, SoldierInline]
    merged_inline_order = 'name'
    merged_field_order = ('alive', 'name', 'house')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Kingdom, KingdomAdmin)
