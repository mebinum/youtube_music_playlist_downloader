from yt_dlp import YoutubeDL, postprocessor


class FilePathCollector(postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilePathCollector, self).__init__(None)
        self.file_paths = []

    def run(self, information):
        self.file_paths.append(information["filepath"])
        return [], information


class SongFileInfo:
    def __init__(self, video_id, name, file_name, file_path, track_num):
        self.video_id = video_id
        self.name = name
        self.file_name = file_name
        self.file_path = file_path
        self.track_num = track_num

    def __repr__(self):
        return f"<SongFileInfo (name={self.name}, file_name={self.file_name},file_path={self.file_path},track_num={self.track_num},video_id={self.video_id})>"


def get_song_info(track_num, link, config: dict):
    # Get song metadata from youtube
    ytdl = get_song_info_ytdl(track_num, config)
    return ytdl.extract_info(link, download=False)


def get_song_info_ytdl(track_num, config: dict):
    # Get ytdl for song info
    name_format = config["name_format"]
    if config["track_num_in_name"]:
        name_format = f"{track_num}. {name_format}"

    ytdl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "outtmpl": name_format,
        "format": config["audio_format"],
        "cookiefile": None if config["cookie_file"] == "" else config["cookie_file"],
        "cookiesfrombrowser": (
            None
            if config["cookies_from_browser"] == ""
            else tuple(config["cookies_from_browser"].split(":"))
        ),
        "writesubtitles": True,
        "allsubtitles": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": config["audio_codec"],
                "preferredquality": config["audio_quality"],
            }
        ],
    }

    info_dict = {}
    return YoutubeDL(ytdl_opts)


def create_file_info(playlist_name, song, config):
    song_info = None
    try:
        song_info = get_song_info(
            song.track_num, f"https://www.youtube.com/watch?v={song.video_id}", config
        )
    except Exception as err:
        print(f"Failed to get song info for '{song.name}'")
        print(f"[err] {err}")

    return {
        "playlist_name": playlist_name,
        "file_name": song.file_name,
        "file_path": song.file_path,
        **song_info,
    }
