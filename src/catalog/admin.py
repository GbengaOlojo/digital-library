from django.contrib import admin

from .models import Book, Author, Genre, Language, BookInstance

# Register models
#admin.site.register(Book)
class BookInstanceInline(admin.TabularInline):
    model =  BookInstance


#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter  = ('status', 'due_back')

    # fieldsets is uded for grouping set of properties in a model object
    fieldsets = (
        ('Book Details' , {
            'fields': ('book', 'id')
        }),
        ('Availability', {
                'fields': ('status', 'due_back')
            })
        )

class BookInline(admin.TabularInline):
    model =  Book
    extra =  0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def get_genres(self, object):
        return ','.join([genres.name for genres in object.genres.all()])
    list_display = ('title', 'author', 'get_genres')
    

# Register models
#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    search_fields = ('last_name',)
    list_filter = ('first_name',)
    inlines = [BookInline]





admin.site.register(Genre)


admin.site.register(Language)


