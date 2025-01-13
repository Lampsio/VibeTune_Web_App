# serializers.py
from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'email', 'description', 'url_image_profile', 
                  'background_image_url', 'telephone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Tworzy użytkownika, wykorzystując metodę `create_user`
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    
class CustomUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'email', 'url_image_profile', 'background_image_url','is_verified' , 'is_banned','followers_count', 'following_count']
    
class CustomUserViewMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'email', 'url_image_profile', 'background_image_url','is_verified' , 'is_banned','followers_count', 'following_count','telephone']
    


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'id', 'name', 'description','url_mp3',  'main_image', 'background_image_url',
            'adult', 'is_public', 'genre', 'duration'
        ]
        read_only_fields = ['id', 'duration']  # czas trwania jest tylko do odczytu



class MusicViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'id', 'name', 'description',  'main_image', 'background_image_url',
            'adult', 'is_public', 'genre', 'duration'
        ]
        read_only_fields = ['id', 'duration']  # czas trwania jest tylko do odczytu

##########

class CustomUserSerializer18(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name', 'lastname']

class MusicWithAuthorSerializer18(serializers.ModelSerializer):
    author = CustomUserSerializer18(source='user')  # Zagnieżdżony serializer dla autora utworu

    class Meta:
        model = Music
        fields = [
            'id', 'name', 'description', 'url_mp3', 'main_image', 'background_image_url',
            'adult', 'is_public', 'genre', 'duration', 'author'
        ]

#########

class PlaylistWithAuthorSerializer18(serializers.ModelSerializer):
    user = CustomUserSerializer18()  # Zagnieżdżony serializer dla autora utworu

    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'is_public', 'is_adult', 'description', 'cover_image',
            'background_image_url', 'user'
        ]

class PlaylistCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'is_public', 'is_adult', 'description', 'cover_image', 'background_image_url']


class AlbumCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['id', 'name', 'is_public', 'is_adult', 'description', 'cover_image', 'background_image_url']

#########


class PlaylistSerializer(serializers.ModelSerializer):
    music_list = MusicSerializer(source='playlistmusic_set.all', many=True)

    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'is_public', 'is_adult', 'description',
            'cover_image', 'background_image_url', 'created_at', 'music_list'
        ]

    def get_music_set(self, obj):
        music_items = obj.music_set.filter(is_public=True)
        return MusicSerializer(music_items, many=True).data
    
class TestPlaylistSerializer(serializers.ModelSerializer):
    music_list = MusicSerializer(many=True)

    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'is_public', 'is_adult', 'description',
            'cover_image', 'background_image_url', 'created_at', 'music_list'
        ]
    
    
class MusicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['name', 'description', 'main_image', 'background_image_url', 'adult', 'is_public', 'genre']

######
class MusicMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'name', 'description', 'url_mp3', 'main_image', 'background_image_url', 'release_date', 'duration', 'genre', 'is_public']

class PlaylistMusicMeSerializer(serializers.ModelSerializer):
    music = MusicMeSerializer()

    class Meta:
        model = PlaylistMusic
        fields = ['music']

class PlaylistMeSerializer(serializers.ModelSerializer):
    playlist_music = PlaylistMusicMeSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'is_adult', 'description', 'cover_image', 'background_image_url', 'created_at','playlist_music']

#####

class CustomUserListenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'is_verified']

class MusicListenSerializer(serializers.ModelSerializer):
    user = CustomUserListenSerializer()  # Zagnieżdżony serializer dla autora utworu

    class Meta:
        model = Music
        fields = ['id', 'name', 'description', 'main_image', 'background_image_url', 'release_date', 'duration', 'genre', 'is_public','is_subtitle', 'user']

class PlaylistMusicListenSerializer(serializers.ModelSerializer):
    music = MusicListenSerializer()  # Użyj MusicListenSerializer zamiast MusicMeSerializer

    class Meta:
        model = PlaylistMusic
        fields = ['music']

class PlaylistListenSerializer(serializers.ModelSerializer):
    user = CustomUserListenSerializer()  # Zagnieżdżony serializer dla autora utworu
    playlist_music = PlaylistMusicListenSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'is_adult', 'is_public', 'description', 'cover_image', 'background_image_url', 'created_at', 'user','playlist_music']

########33

class MusicDetailSerializer(serializers.ModelSerializer):
    user = CustomUserListenSerializer()  # Zagnieżdżony serializer dla autora utworu

    class Meta:
        model = Music
        fields = [
            'id', 'name', 'description', 'main_image', 'background_image_url',
            'adult', 'is_public', 'genre', 'duration','release_date','is_subtitle','user'
        ]
        read_only_fields = ['id', 'duration']  # czas trwania jest tylko do odczytu

############
class MusicUpdateSubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['is_subtitle']
###########

class AlbumMusicMeSerializer(serializers.ModelSerializer):
    music = MusicMeSerializer()

    class Meta:
        model = AlbumMusic
        fields = ['music']

class AlbumMeSerializer(serializers.ModelSerializer):
    playlist_album = AlbumMusicMeSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'is_adult', 'description', 'cover_image', 'background_image_url', 'created_at','playlist_album']

#####

class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'email', 'url_image_profile', 'background_image_url']

class MusicSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'name', 'description', 'url_mp3', 'main_image', 'background_image_url', 'release_date', 'duration', 'genre', 'is_public']

class PlaylistMusicSerializer1(serializers.ModelSerializer):
    music = MusicSerializer1()

    class Meta:
        model = PlaylistMusic
        fields = ['music']

class PlaylistSerializer(serializers.ModelSerializer):
    user = UserSerializer1()
    playlist_music = PlaylistMusicSerializer1(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'is_public', 'is_adult', 'description', 'cover_image', 'background_image_url', 'created_at', 'user', 'playlist_music']
######

class PlaylistUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['name', 'is_public', 'is_adult', 'description', 'cover_image', 'background_image_url']

class PlaylistMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistMusic
        fields = ['id', 'playlist', 'music']  # Pola do zdefiniowania relacji
        read_only_fields = ['id']  # `id` jest tylko do odczytu

    def validate(self, data):
        # Sprawdzamy, czy utwór już istnieje w danej playliście
        if PlaylistMusic.objects.filter(playlist=data['playlist'], music=data['music']).exists():
            raise serializers.ValidationError("Ten utwór już znajduje się w tej playliście.")
        return data
    
class FavoritePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePlaylist
        fields = ['id', 'playlist', 'user']
        read_only_fields = ['id', 'user']  # Użytkownik będzie automatycznie ustawiany na aktualnie zalogowanego

    def validate(self, data):
        # Sprawdzenie, czy użytkownik nie próbuje dodać swojej własnej playlisty
        if data['playlist'].user == self.context['request'].user:
            raise serializers.ValidationError("Nie możesz dodać swojej własnej playlisty do ulubionych.")
        return data
    
class FavoritePlaylistDetailSerializer(serializers.ModelSerializer):
    playlist_id = serializers.CharField(source='playlist.id', read_only=True)
    main_image = serializers.ImageField(source='playlist.cover_image', read_only=True)
    playlist_name = serializers.CharField(source='playlist.name', read_only=True)
    author_name = serializers.SerializerMethodField()
    is_adult = serializers.BooleanField(source='playlist.is_adult', read_only=True)

    class Meta:
        model = FavoritePlaylist
        fields = ['id','playlist_id', 'main_image', 'playlist_name', 'author_name', 'is_adult']

    def get_author_name(self, obj):
        return f"{obj.playlist.user.name} {obj.playlist.user.lastname}"
    
class PlaylistAssignmentSerializer(serializers.ModelSerializer):
    is_music_assigned = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'is_music_assigned']

    def get_is_music_assigned(self, obj):
        music_id = self.context.get('music_id')
        return PlaylistMusic.objects.filter(playlist=obj, music_id=music_id).exists()
    
    
#############

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follows
        fields = ['follower', 'following', 'date_follow']


class FollowSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Follows
        fields = ['following']

class CustomUserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'url_image_profile']


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'name', 'description','link_url']

class VerifyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = []  # No fields are required from the input

class CustomUserModSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname']

class VerifySerializer(serializers.ModelSerializer):
    user = CustomUserModSerializer()
    moderator = CustomUserModSerializer()

    class Meta:
        model = Verify
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    sender = CustomUserModSerializer()
    moderator = CustomUserModSerializer()

    class Meta:
        model = Report
        fields = '__all__'

class VerifyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = ['status']

class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['status']


##################

class CustomUserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'lastname', 'url_image_profile']

class PlaylistSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'cover_image']

class AlbumSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'cover_image']

class MusicSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'name', 'main_image']
