# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView1.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #endpoint na odświeżenie tokena

    path('api/users/', CustomUserListTopView.as_view(), name='user18-list'),
    path('api/user/<str:user_id>/', UserView.as_view(), name='user-view'),
    path('api/user/me', UserMe.as_view(), name='user-view-me'),
    
    path('api/music/', MusicCreateView.as_view(), name='music-create'),
    path('api/musics/', MusicListWithAuthorView18.as_view(), name='music18-list'),
    path('api/music/<str:pk>/update/', MusicUpdateView.as_view(), name='music-update'),
    path('api/music/<str:pk>/delete/', MusicDeleteView.as_view(), name='music-delete'),
    path('api/music/user/<str:user_id>/', ListUserMusicView.as_view(), name='user-music-list'),
    path('api/music/<str:id>/', MusicDetailView.as_view(), name='music-detail'),
    path('api/music/update_subtitle/<str:pk>/', MusicUpdateSubtitleView.as_view(), name='music-update-subtitle'),
    path('api/music/stream/<str:id>/', StreamMusicView.as_view(), name='music-stream'),


    path('api/playlist/', PlaylistCreateView.as_view(), name='create_playlist'),
    path('api/playlists/', PlaylistListWithAuthorView18.as_view(), name='playlist18-list'),
    path('playlist/<int:pk>/update/', PlaylistUpdateView.as_view(), name='update_playlist'),
    path('playlist/<int:pk>/delete/', PlaylistDeleteView.as_view(), name='delete_playlist'),
    path('api/playlist/user/<str:user_id>/', ListUserPlayMusicView.as_view(), name='user-music-list'),
    path('api/playlists/listen/<str:pk>/', PlaylistDetailListenView.as_view(), name='playlist-detail'),
    path('api/playlist/user/detail/<str:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('api/playlist/me', ListMePlaylistView.as_view(), name='playlist-detail-me'),
    

    path('api/playlistmusic/' , AddMusicToPlaylistView.as_view(), name='add_music_playlist'),
    path('api/playlistmusic/<int:pk>/delete', RemoveMusicFromPlaylistView.as_view(), name='remove-music-from-playlist'),
    path('api/playlistmusic/music/<str:music_id>/', PlaylistWithMusicAssignmentView.as_view(), name='playlists_with_music_assignment'),

    path('api/album/', AlbumCreateView.as_view(), name='album-create'),
    path('api/album/user/<str:user_id>/', ListUserAlbumView.as_view(), name='user-album-list'),

    path('api/favorites/', AddFavoritePlaylistView.as_view(), name='add-favorite-playlist'),
    path('api/favorites/remove/<int:pk>/', RemoveFavoritePlaylistView.as_view(), name='remove-favorite-playlist'),
    path('api/favorites/list/', ListFavoritePlaylistsView.as_view(), name='list-favorite-playlists'),

    path('api/follow/', FollowCreateView.as_view(), name='follow-create'),
    path('api/follow/remove/<str:following_id>/', FollowDeleteView.as_view(), name='follow-delete'),
    path('api/follow/list/', FollowListView.as_view(), name='follow-list'),
    path('api/follow/check/<str:following_id>/', CheckFollowView.as_view(), name='follow-check'),

    path('api/reports/create', ReportCreateView.as_view(), name='report-create'),
    path('api/reports/', ReportListView.as_view(), name='report-list'),
    path('api/reports/<str:pk>/update/', ReportUpdateView.as_view(), name='report-update'),

    path('api/verify/create', VerifyCreateView.as_view(), name='report-create'),
    path('api/verify/', VerifyListView.as_view(), name='verify-list'),
    path('api/verify/<str:pk>/update/', VerifyUpdateView.as_view(), name='verify-update'),

    path('api/search/', SearchView.as_view(), name='search'),

    path('dane/', DaneView.as_view(), name='dane'),
]
