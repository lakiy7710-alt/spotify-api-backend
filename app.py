from fastapi import FastAPI
import yt_dlp
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS for Android App connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Spotify Backend is Running!"}

# NEW: Search logic jo tumhare App ko chahiye
@app.get("/search")
def search_songs(q: str):
    try:
        ydl_opts = {
            'quiet': True, 
            'noplaylist': True,
            'extract_flat': True, # Fast search ke liye
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # YouTube se top 10 results nikalega
            results = ydl.extract_info(f"ytsearch10:{q}", download=False)['entries']
            
            output = []
            for entry in results:
                output.append({
                    "id": entry.get('id'),
                    "title": entry.get('title'),
                    "artist": entry.get('uploader', 'Unknown Artist'),
                    "imageUrl": entry.get('thumbnail', ''),
                    "spotifyUrl": f"https://youtube.com{entry.get('id')}",
                    "durationMs": int(entry.get('duration', 0)) * 1000
                })
            return output
    except Exception as e:
        return {"error": str(e)}

# Existing Stream logic
@app.get("/get_stream")
def get_stream(spotify_url: str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{spotify_url}", download=False)['entries'][0]
            return {
                "url": info['url'], 
                "title": info['title'],
                "thumbnail": info.get('thumbnail', ""),
                "status": "success"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
