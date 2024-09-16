# Video Upload and Processing Website

This project is a web application that allows users to upload videos, process them to extract subtitles in multiple languages, and display those subtitles as closed captions. The user can also search for specific phrases within the subtitles and get timestamps where those phrases appear in the video.

## Features

- **Video Upload**: Users can upload video files through the frontend.
- **Subtitle Extraction**: Extracts subtitles in multiple languages using `ffmpeg`.
- **Search Functionality**: Allows users to search for phrases in the subtitles and retrieve timestamps.
- **Video Streaming**: Videos can be streamed from the backend.
- **List View**: Displays a list of uploaded videos with available subtitle languages.
- **Multi-language Subtitles**: Subtitles in multiple languages can be processed and viewed.
- **Dockerized Setup**: The application uses Docker for containerized development and deployment.

## Stack

- **Backend**: Django with PostgreSQL
- **Frontend**: React
- **Video Processing**: `ffmpeg` for extracting subtitles
- **Database**: PostgreSQL for storing subtitles and video metadata
- **Containerization**: Docker and Docker Compose

## Prerequisites

- Docker installed on your system.
- ffmpeg installed in the Docker container for subtitle extraction.

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/shashankusinggithub/video-processing-app.git
   cd video-processing-app
   ```

2. Modify the `.env` file to set your PostgreSQL database credentials (e.g., `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_HOST`, `DATABASE_PORT`).

   ```
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   DATABASE_HOST=db
   DATABASE_PORT=5432
   ```

3. Run the provided `.sh` script to build, migrate the database, and start the Docker containers:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## API Endpoints

- **Upload Video**: `/api/upload/` (POST) - Upload a video file.
- **List Videos**: `/api/videos/` (GET) - Fetch list of uploaded videos with available subtitle languages.
- **Get Video**: `/api/videos/<str:subtitle_id>/` (GET) - Get the subtitle file.
- **Get Subtitle**: `/api/videos/<str:video_id>/` (GET) - Get the video file.
- **Search Subtitles**: `/api/search-subtitle/` (GET) - Search for a phrase within a video’s subtitles.

## Frontend Features

- **Video List**: Displays all uploaded videos with their titles and the number of subtitle languages.
- **Video Player**: Streams the video and displays corresponding subtitles.
- **Search**: Search for specific words or phrases within the subtitles.
-

## Nginx

The project uses Nginx as a reverse proxy to serve the React frontend and proxy requests to the Django backend. The Nginx configuration is included in the Docker setup.

**Nginx Configuration:**

- **Reverse Proxy**: Nginx proxies requests from `http://localhost` to the Django backend and serves static files for the React frontend.
- **Configuration File**: The Nginx configuration file is located at `nginx/nginx.conf`.

Ensure that the `nginx/nginx.conf` file is correctly configured to handle requests and serve the appropriate services.

## Running the Project

1. Clone the repository and navigate to the project directory.
2. Ensure that the `.env` file contains your PostgreSQL configuration (or create it).
3. Run the `run.sh` script:
   ```bash
   ./run.sh
   ```

This script will:

- Build the Docker containers for the Django backend, React frontend, PostgreSQL database and Nginx Proxy.
- Run database migrations.
- Start all services.

4. Access the app via `http://localhost`
