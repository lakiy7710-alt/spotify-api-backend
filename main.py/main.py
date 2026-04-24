from fastapi import FastAPI
import yt_dlp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Taaki aapka Android app isse connect kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Spotify Backend is Running!"}

@app.get("/get_stream")
def get_stream(spotify_url: str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ye Spotify link ko YouTube par search karke audio nikalega
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
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
