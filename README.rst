|Build Status| |Coverage Status| |PyPI version|

Merged Inlines
==============

Merged Inlines is a Django App that allows you to merge multiple inline
models into a single form. This is particularly useful if you need to
mix the orderings of multiple authors together, so your inlines in the
Admin panel can look like:

-  inline for Poem 1
-  inline for Poem 2
-  inline for Book 1
-  inline for Poem 3
-  inline for Book 2

Instead of:

-  inline for Poem 1
-  inline for Poem 2
-  inline for Poem 3

-  inline for Book 1
-  inline for Book 2

Installation
------------

Install using pip:

::

    pip install django-merged-inlines

Quick start
-----------

1. Add "merged\_inlines" to your INSTALLED\_APPS setting:

::

    INSTALLED_APPS = (
        ....
        'merged_inlines'
    )

2. In the admin.py file for the app you're adding merged inlines to,
   add:

::

    from merged_inlines.admin import MergedInlineAdmin

3. Instead of admin.ModelAdmin, make your Admin class a child of
   MergedInlineAdmin, and add your inline classes as you normally would:

::

    class MyFirstInline(admin.TabularInline):
        pass

    class MySecondInline(admin.TabularInline):
        pass

    class MyModelAdmin(MergedInlineAdmin):
        inlines = [MyFirstInline,MySecondInline]

    admin.site.register(MyModel,MyModelAdmin)

Note that regardless of the Inline class used (TabularInline or
StackedInline), Merged Inlines currently only renders as a tabular
inline.

Options
-------

merged\_field\_order
~~~~~~~~~~~~~~~~~~~~

You can use merged\_field\_order in your MergedInlineAdmin class to set
the order of the fields. The list/type must contain all of fields that
will be editable in the admin: to exclude fields from the formset, use
the builtin ModelAdmin ``exclude`` function.

::

    class MyInline(admin.TabularInline):
        exclude = ('my_unwanted_field')

    class MyModelAdmin(MergedInlineAdmin):
        inlines = [MyInline]

        merged_field_order = ('put_this_field_first','followed_by_this_field','and_then_this_one')

merged\_inline\_order
~~~~~~~~~~~~~~~~~~~~~

This option determines what field will be used to sort your merged
inline models. The shared models must both have the shared field,
otherwise an Exception will be raised. If no field is specified, ``id``
will be used.

::

    class BookInline(admin.TabularInline):
        model = Book

    class PoemInline(admin.TabularInline):
        model = Poem

    class AuthorAdmin(MergedInlineAdmin):
        merged_inline_order = 'year'

Version History

-  1.0 - Added full test coverage. Moved to Django 1.7+ compatibility,
   dropped compatibility with Django <1.7.
-  0.2 - Fixed ID ordering and js issues, thanks to @kotyy
-  0.1 - Initial release

.. |Build Status| image:: https://travis-ci.org/MattBroach/Django-Merged-Inlines.svg?branch=master
   :target: https://travis-ci.org/MattBroach/Django-Merged-Inlines
.. |Coverage Status| image:: https://coveralls.io/repos/github/MattBroach/Django-Merged-Inlines/badge.svg?branch=master
   :target: https://coveralls.io/github/MattBroach/Django-Merged-Inlines?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/django-merged-inlines.svg
   :target: https://badge.fury.io/py/django-merged-inlines
