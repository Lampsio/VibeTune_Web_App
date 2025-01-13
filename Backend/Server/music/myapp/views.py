# views.py
from rest_framework import status ,  permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView , DestroyAPIView , ListAPIView , RetrieveAPIView , CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.http import FileResponse, Http404
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import *

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Tylko właściciel obiektu może go edytować
        return obj.user == request.user

class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            # Tworzy nowego użytkownika, korzystając z `create_user`
            user = serializer.save()
            return Response({"message": "Użytkownik został utworzony pomyślnie."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Sprawdź poprawność danych uwierzytelniających
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generowanie tokenów JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Nieprawidłowy email lub hasło."}, status=status.HTTP_401_UNAUTHORIZED)
        
class LoginView1(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Sprawdź poprawność danych uwierzytelniających
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generowanie tokenów JWT
            refresh = RefreshToken.for_user(user)

            # Dodanie ról do tokenu
            roles = list(user.groups.values_list('name', flat=True))
            refresh["roles"] = roles  # Dodajemy role do payload tokenu

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Nieprawidłowy email lub hasło."}, status=status.HTTP_401_UNAUTHORIZED)
        
class MusicCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            music = serializer.save(user=request.user)  # przypisanie użytkownika
            music.save()  # zapisz, co również obliczy `duration`
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserMe(APIView):
    serializer_class = CustomUserViewMeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Pobiera ulubione playlisty zalogowanego użytkownika
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
class MusicUpdateView(UpdateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MusicDeleteView(DestroyAPIView):
    queryset = Music.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Music deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ListUserMusicView(ListAPIView):
    serializer_class = MusicViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')  # Pobiera user_id z URL
        current_user = self.request.user  # Pobiera aktualnie zalogowanego użytkownika

        if str(current_user.id) == user_id:
            # Jeśli user_id z URL jest taki sam jak user_id z tokena, zwróć wszystkie playlisty
            queryset = Music.objects.filter(user__id=user_id)
        else:
            # Jeśli user_id z URL jest różny od user_id z tokena, zwróć tylko publiczne playlisty
            queryset = Music.objects.filter(user__id=user_id, is_public=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListUserAlbumView(ListAPIView):
    serializer_class = AlbumMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')  # Pobiera user_id z URL
        current_user = self.request.user  # Pobiera aktualnie zalogowanego użytkownika

        if str(current_user.id) == user_id:
            # Jeśli user_id z URL jest taki sam jak user_id z tokena, zwróć wszystkie playlisty
            queryset = Album.objects.filter(user__id=user_id)
        else:
            # Jeśli user_id z URL jest różny od user_id z tokena, zwróć tylko publiczne playlisty
            queryset = Album.objects.filter(user__id=user_id, is_public=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class UserView(ListAPIView):
    serializer_class = CustomUserViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Pobiera user_id z URL
        return CustomUser.objects.filter(id=user_id)
    
class MusicDetailView(RetrieveAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # Użyjemy pola 'id' do wyszukiwania

class MusicUpdateSubtitleView(UpdateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicUpdateSubtitleSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ListMePlaylistView(ListAPIView):
    serializer_class = PlaylistMeSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        # Filtrowanie playlist, które należą do aktualnie zalogowanego użytkownika
        user = self.request.user
        return Playlist.objects.filter(user=user)


class ListUserPlayMusicView(ListAPIView):
    serializer_class = PlaylistMeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')  # Pobiera user_id z URL
        current_user = self.request.user  # Pobiera aktualnie zalogowanego użytkownika

        if str(current_user.id) == user_id:
            # Jeśli user_id z URL jest taki sam jak user_id z tokena, zwróć wszystkie playlisty
            queryset = Playlist.objects.filter(user__id=user_id)
        else:
            # Jeśli user_id z URL jest różny od user_id z tokena, zwróć tylko publiczne playlisty
            queryset = Playlist.objects.filter(user__id=user_id, is_public=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PlaylistDetailView(APIView):
    def get(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk , is_public=True)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PlaylistCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PlaylistCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Przypisujemy użytkownika jako właściciela playlisty
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AlbumCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AlbumCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Przypisujemy użytkownika jako właściciela playlisty
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlaylistUpdateView(UpdateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlaylistDeleteView(DestroyAPIView):
    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Playlist deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class AddMusicToPlaylistView(APIView):
    permission_classes = [IsAuthenticated]  # Tylko zalogowani użytkownicy mogą dodawać utwory

    def post(self, request, *args, **kwargs):
        serializer = PlaylistMusicSerializer(data=request.data)
        
        # Sprawdzamy, czy dane są poprawne
        if serializer.is_valid():
            serializer.save()  # Zapisuje relację Playlist-Music
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Jeśli dane są niepoprawne, zwracamy błędy
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveMusicFromPlaylistView(DestroyAPIView):
    queryset = PlaylistMusic.objects.all()
    permission_classes = [IsAuthenticated]  # Tylko zalogowani użytkownicy mogą usuwać utwory

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Pobieramy obiekt do usunięcia
        self.perform_destroy(instance)  # Usuwamy obiekt
        return Response({"detail": "Utwór został usunięty z playlisty."}, status=status.HTTP_204_NO_CONTENT)
    
class AddFavoritePlaylistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FavoritePlaylistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Dodajemy playlistę do ulubionych przypisaną do zalogowanego użytkownika
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFavoritePlaylistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            favorite_playlist = FavoritePlaylist.objects.get(id=pk)
        except FavoritePlaylist.DoesNotExist:
            return Response({"detail": "Ulubiona playlista nie została znaleziona lub nie należy do Ciebie."},
                            status=status.HTTP_404_NOT_FOUND)

        favorite_playlist.delete()
        return Response({"detail": "Playlista została usunięta z ulubionych."}, status=status.HTTP_204_NO_CONTENT)
    
class ListFavoritePlaylistsView(ListAPIView):
    serializer_class = FavoritePlaylistDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Pobiera ulubione playlisty zalogowanego użytkownika
        return FavoritePlaylist.objects.filter(user=self.request.user).select_related('playlist', 'playlist__user')
    
class CustomUserListView0(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserViewSerializer

class CustomUserListTopView(ListAPIView):
    serializer_class = CustomUserViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Pobierz tylko 10 użytkowników
        return CustomUser.objects.all()[:18]
    
    
class MusicListWithAuthorView18(ListAPIView):
    serializer_class = MusicWithAuthorSerializer18

    def get_queryset(self):
        # Pobierz utwory muzyczne, a także załaduj dane autora
        return Music.objects.prefetch_related('user').all()[:18]  # Możesz ustawić odpowiednią liczbę
    
class PlaylistListWithAuthorView18(ListAPIView):
    serializer_class = PlaylistWithAuthorSerializer18

    def get_queryset(self):
        # Pobierz utwory muzyczne, a także załaduj dane autora
        return Playlist.objects.prefetch_related('user').all()[:18]  # Możesz ustawić odpowiednią liczbę
    
class StreamMusicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            # Pobierz obiekt Music na podstawie ID
            music = Music.objects.get(id=id) 
            file_path = music.url_mp3.path  # Pełna ścieżka do pliku
            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        except Music.DoesNotExist:
            raise Http404("Music not found.")
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
class PlaylistDetailListenView(RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistListenSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        playlist = self.get_object()

        if not playlist.is_public:
            if playlist.user != request.user:
                raise PermissionDenied("You do not have permission to access this playlist.")

        return self.retrieve(request, *args, **kwargs)

class PlaylistWithMusicAssignmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, music_id, *args, **kwargs):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistAssignmentSerializer(playlists, many=True, context={'music_id': music_id})
        return Response(serializer.data)
    
###############3

class DaneView(APIView):
    permission_classes = [IsAuthenticated]  # Tylko zalogowani użytkownicy mają dostęp
    
    def get(self, request, *args, **kwargs):
        # Przykładowe dane zwracane tylko dla zalogowanych użytkowników
        dane = {
            "message": "Masz dostęp do tych danych, ponieważ jesteś zalogowany.",
            "user": request.user.email,
        }
        return Response(dane, status=status.HTTP_200_OK)
    

################


class FollowCreateView(CreateAPIView):
    queryset = Follows.objects.all()
    serializer_class = FollowSerializer1
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class FollowDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, following_id, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(Follows, follower=follower, following_id=following_id)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FollowListView(ListAPIView):
    serializer_class = CustomUserFollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(followers__follower=self.request.user)

class CheckFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, following_id, *args, **kwargs):
        follower = request.user
        following_exists = Follows.objects.filter(follower=follower, following_id=following_id).exists()
        return Response({'is_following': following_exists}, status=status.HTTP_200_OK)
    
class ReportCreateView(CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user,type='User')

class VerifyCreateView(CreateAPIView):
    queryset = Verify.objects.all()
    serializer_class = VerifyCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VerifyListView(ListAPIView):
    queryset = Verify.objects.all()
    serializer_class = VerifySerializer
    permission_classes = [IsAuthenticated]

class ReportListView(ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

class VerifyUpdateView(UpdateAPIView):
    queryset = Verify.objects.all()
    serializer_class = VerifyUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.status = serializer.validated_data.get('status', instance.status)
        instance.moderator = self.request.user
        instance.save()

class ReportUpdateView(UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.status = serializer.validated_data.get('status', instance.status)
        instance.moderator = self.request.user
        instance.save()

class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        users = CustomUser.objects.filter(Q(name__icontains=query) | Q(lastname__icontains=query))
        playlists = Playlist.objects.filter(name__icontains=query)
        albums = Album.objects.filter(name__icontains=query)
        music = Music.objects.filter(name__icontains=query)

        users_serializer = CustomUserSearchSerializer(users, many=True)
        playlists_serializer = PlaylistSearchSerializer(playlists, many=True)
        albums_serializer = AlbumSearchSerializer(albums, many=True)
        music_serializer = MusicSearchSerializer(music, many=True)

        return Response({
            "users": users_serializer.data,
            "playlists": playlists_serializer.data,
            "albums": albums_serializer.data,
            "music": music_serializer.data
        })
