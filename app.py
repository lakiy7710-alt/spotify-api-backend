from fastapi import FastAPI, Query
import yt_dlp
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Spotify Backend is Running!"}

@app.get("/search")
def search_songs(q: str = Query(...)):
    try:
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "skip_download": True,
            "format": "bestaudio/best",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(f"ytsearch10:{q}", download=False)
            results = data.get("entries", [])

            output = []
            for entry in results:
                video_id = entry.get("id")
                if not video_id:
                    continue

                output.append({
                    "id": video_id,
                    "title": entry.get("title") or "Unknown Title",
                    "artist": entry.get("uploader") or entry.get("channel") or "Unknown Artist",
                    "imageUrl": entry.get("thumbnail") or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                    "spotifyUrl": f"https://www.youtube.com/watch?v={video_id}",
                    "durationMs": int(entry.get("duration") or 0) * 1000
                })

            return output

    except Exception as e:
        return {"error": str(e)}

@app.get("/get_stream")
def get_stream(spotify_url: str):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(spotify_url, download=False)

            return {
                "url": info.get("url"),
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail", ""),
                "status": "success"
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
