@app.get("/search")
def search_songs(q: str):
    try:
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            # 'extract_flat' ko hata diya hai taaki images mil sakein
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # search results nikalna
            results = ydl.extract_info(f"ytsearch10:{q}", download=False)['entries']
            
            output = []
            for entry in results:
                # Thumbnail nikalne ka sabse safe tarika
                thumb = entry.get('thumbnail') or (entry.get('thumbnails')[0]['url'] if entry.get('thumbnails') else '')
                
                output.append({
                    "id": entry.get('id'),
                    "title": entry.get('title'),
                    "artist": entry.get('uploader', 'Unknown Artist'),
                    "imageUrl": thumb,  # Ab image URL khali nahi jayega
                    "streamUrl": entry.get('url'), # Playback ke liye
                    "durationMs": int(entry.get('duration', 0)) * 1000
                })
            return output
    except Exception as e:
        return {"error": str(e)}
