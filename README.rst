==============
Merged Inlines
==============

Merged Inlines is a Django App that allows you to merge multiple inline models into a single form.  This is particularly useful if you need to mix the orderings of multiple authors together, so your inlines in the Admin panel can look like:

 - inline for Poem 1
 - inline for Poem 2
 - inline for Book 1
 - inline for Poem 3
 - inline for Book 2

Instead of:

- inline for Poem 1
- inline for Poem 2
- inline for Poem 3

- inline for Book 1
- inline for Book 2


Installation
-------------

Install using pip:

    pip install django-merged-inlines

Quick start
-----------

1. Add "merged_inlines" to your INSTALLED_APPS setting:

    INSTALLED_APPS = (
        ....
        'merged_inlines'
    )

2. In the admin.py file for the app you're adding merged inlines to, add:

    from merged_inlines.admin import MergedInlineAdmin

3. Instead of admin.ModelAdmin, make your Admin class a child of MergedInlineAdmin, and add your inline classes as you normally would:

    class MyFirstInline(admin.TabularInline):
        pass

    class MySecondInline(admin.TabularInline):
        pass

    class MyModelAdmin(MergedInlineAdmin):
        inlines = [MyFirstInline,MySecondInline]

    admin.site.register(MyModel,MyModelAdmin)

Note that regardless of the Inline class used (TabularInline or StackedInline), Merged Inlines currently only renders as a tabular inline.

Options
-------

You can use merged_field_order in your MergedInlineAdmin class to set the order of the fields.  The fields can be ordering of the fields in all your inlines.  However, it is recommended that if you have fields you wish to not show up in the admin panel, you exclude them in your inline classes:

    class MyInline(admin.TabularInline):
        exclude = ('my_unwanted_field')

    class MyModelAdmin(MergedInlineAdmin):
        inlines = [MyInline]

        merged_field_order = ('put_this_field_first','followed_by_this_field','and_then_this_one')

You can also specify which field you'd like to use to order your differen inlines using merged_inline_order.  So the following would list the poems and books by a certain author, sorted by year:

    class BookInline(admin.TabularInline):
        model = Book

    class PoemInline(admin.TabularInline):
        model = Poem

    class AuthorAdmin(MergedInlineAdmin):
        merged_inline_order = 'year'

Of course, both the Poem and Book models need to have a 'year' field for the above to work.  If no value for merged_inline_order is given, it will default to sorting by object id.


