# Vision AI Backend Rest API



- JWT authentication
- Translation of audio to any language
- YouTube video hashtag generation
- YouTube video description generation
- YouTube video script generation

## Features

### JWT Authentication

The API uses JSON Web Token (JWT) authentication to secure the endpoints. Users need to obtain a valid JWT token by providing their credentials through the appropriate endpoint. This token must be included in the `Authorization` header for subsequent requests to access protected routes.

### Translation of Audio

The API provides functionality to translate audio content to any language of the user's liking. Users can submit an audio file to the API, specifying the source language and the target language they want to translate to. The API will process the audio and return the translated version.

### YouTube Video Hashtag Generation

Users can generate relevant hashtags for YouTube videos using this API. By providing a title or a description of the video, the API will analyze the content and generate a list of popular and related hashtags that can help increase the video's discoverability on the platform.

### YouTube Video Description Generation

This API feature allows users to generate a descriptive summary for YouTube videos. Users can provide the title, content, or any relevant information about the video, and the API will generate an optimized description that can be used to enhance the video's metadata.

### YouTube Video Script Generation

Users can generate a script for YouTube videos using this API. By providing a video URL or the video ID, the API will extract the audio content from the video and generate a transcript or script. This feature can be useful for creating captions, subtitles, or planning the structure of video content.

## Running the App Locally

To run this application locally, please follow these steps:

1. Clone the repository:

   ```
   $ git clone https://github.com/NithinYesudas/VisionAI_backend
   ```

2. Navigate to the project directory:

   ```
   $ cd your-repo
   ```

3. Create a virtual environment:

   ```
   $ python3 -m venv venv
   ```

4. Activate the virtual environment:

   - For Linux/macOS:

     ```
     $ source venv/bin/activate
     ```

   - For Windows:

     ```
     $ venv\Scripts\activate
     ```

5. Install the required dependencies:

   ```
   $ pip install -r requirements.txt
   ```

6. Set up the necessary environment variables. Create a `.env` file in the project's root directory and define the following variables:

   ```
   SECRET_KEY=<your-secret-key>
   ```

   Replace `<your-secret-key>` with your preferred secret key for JWT token encryption.

7. Start the application:

   ```
   $ uvicorn main:app --reload
   ```

   The API will be accessible at `http://localhost:8000`.

8. Use a tool like cURL, Postman, or your preferred HTTP client to interact with the API endpoints.

## API Documentation

Once the application is running locally, you can access the API documentation at `http://localhost:8000/docs`. The documentation provides details on the available endpoints, request/response formats, and authentication requirements.

Please ensure you have a valid JWT token to access the protected routes. Refer to the API documentation for the authentication process.

