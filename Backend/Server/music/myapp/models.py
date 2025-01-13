from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group
from mutagen.mp3 import MP3  # mutagen pozwala na analizę plików audio, w tym MP3
import ulid 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Adres email jest wymagany")
        email = self.normalize_email(email)
        # Ustaw ULID jako ID użytkownika
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        # Zapisz użytkownika przed dodaniem go do grupy, aby miał ID
        user.save(using=self._db)
        
        # Dodaj użytkownika do grupy "Normal"
        normal_group, created = Group.objects.get_or_create(name='Normal')
        user.groups.add(normal_group)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

def generate_ulid():
    return ulid.new().str

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid)
    name = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    url_image_profile = models.ImageField(upload_to='images/', blank=True, null=True)
    background_image_url = models.ImageField(upload_to='images/', blank=True, null=True)
    is_banned = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    telephone = models.CharField(max_length=255, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} {self.lastname}"

class UserVerify(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=ulid.new().str)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    status = models.CharField(max_length=20)
    moderator = models.ForeignKey(CustomUser, related_name='verifies', on_delete=models.SET_NULL, null=True)
    link_url = models.CharField(max_length=255)

    def __str__(self):
        return f"Verification for {self.user.email}"


class Music(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    url_mp3 = models.FileField(upload_to='music/', blank=True, null=True)
    main_image = models.ImageField(upload_to='images/', blank=True, null=True)
    background_image_url = models.ImageField(upload_to='images/', blank=True, null=True)
    release_date = models.DateField(auto_now_add=True)
    duration = models.IntegerField(blank=True, null=True)  # trzymamy czas trwania w sekundach
    adult = models.BooleanField(default=False)
    genre = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, related_name='music_set',on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    is_subtitle = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatyczne obliczenie czasu trwania pliku MP3
        if self.url_mp3:
            audio = MP3(self.url_mp3)
            self.duration = int(audio.info.length)  # czas trwania w sekundach
        super().save(*args, **kwargs)


class Tags(models.Model):
    id = models.BigAutoField(primary_key=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid)
    name = models.CharField(max_length=60)
    is_public = models.BooleanField(default=True)
    is_adult = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    background_image_url = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlaylistMusic(models.Model):
    id = models.BigAutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE ,related_name='playlist_music')
    music = models.ForeignKey(Music, on_delete=models.CASCADE,related_name='playlist_music')

    def __str__(self):
        return f"{self.playlist.name} - {self.music.name}"


class Album(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid)
    name = models.CharField(max_length=60)
    is_public = models.BooleanField(default=True)
    is_adult = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    background_image_url = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AlbumMusic(models.Model):
    id = models.BigAutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,related_name='playlist_album')
    music = models.ForeignKey(Music, on_delete=models.CASCADE,related_name='playlist_album')


class Report(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid)
    sender = models.ForeignKey(CustomUser, related_name='reports', on_delete=models.CASCADE)
    release_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    link_url = models.CharField(max_length=255)
    moderator = models.ForeignKey(CustomUser, related_name='report_modifications', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='Waiting')

    def __str__(self):
        return self.name


class Follows(models.Model):
    id = models.BigAutoField(primary_key=True)
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    date_follow = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')


class FavoritePlaylist(models.Model):
    id = models.BigAutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class FavoriteAlbum(models.Model):
    id = models.BigAutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Verify(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    moderator = models.ForeignKey(CustomUser, related_name='verification_modifications', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='Waiting')

    def __str__(self):
        return f"Verification for {self.user.email}" if self.user else "Verification"