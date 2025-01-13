# Vibetune

## Overview
Vibetune is a web application designed for music enthusiasts, allowing users to listen to music, create and customize their profiles, add their own music, create playlists, and manage albums. The application supports continuous music playback even when navigating away from the music page within the app. Users can add lyrics to their music, shuffle tracks, adjust volume, and add playlists to their favorites. Vibetune operates on a microservices architecture using FastAPI and Django.

## Features
- **User Profiles**: Create and customize your own profile.
- **Music Upload**: Add your own music to the platform.
- **Playlist Management**: Create and manage your own playlists.
- **Album Management**: Add and manage albums.
- **Continuous Playback**: Music continues to play even when navigating within the app.
- **Lyrics**: Add lyrics to your music.
- **Shuffle and Volume Control**: Shuffle tracks and adjust volume.
- **Favorites**: Add playlists to your favorites.

## Technologies
- **Django**: Main backend server.
- **FastAPI**: Secondary backend server responsible for lyrics.
- **Docker**: Used for containerizing the database.
- **PostgreSQL**: Used for storing music and user data.
- **Cassandra**: Used for storing lyrics data.
- **TypeScript**: Used for type-safe JavaScript development.
- **Tailwind CSS**: Utility-first CSS framework for styling.
- **React**: JavaScript library for building user interfaces.

## Setup

### Prerequisites
- Docker
- Node.js and npm (for React and TypeScript)
- Python 3.8 or higher (for Django and FastAPI)
