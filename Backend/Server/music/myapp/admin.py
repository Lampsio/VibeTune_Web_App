from django.contrib import admin
from .models import CustomUser , Music , Playlist , Report , Verify

# Opcjonalna klasa do dostosowywania wyświetlania modelu w panelu admina
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'email', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'name', 'lastname')
    list_filter = ('is_staff', 'is_active', 'is_banned', 'is_verified')
    ordering = ('email',)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'url_mp3', 'main_image', 'background_image_url', 'release_date', 'duration', 'adult', 'genre' , 'user' ,'is_public','is_subtitle')
    readonly_fields = ('release_date','user')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_public', 'is_adult', 'description', 'cover_image', 'background_image_url', 'created_at', 'user')
    readonly_fields = ('created_at','user')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'release_date', 'name', 'description', 'type', 'link_url', 'moderator', 'status')
    readonly_fields = ('release_date','sender')

class VerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'moderator','status')
    readonly_fields = ('id', 'user', 'date', 'moderator','status')
    
# Rejestracja modelu
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Verify,VerAdmin)
