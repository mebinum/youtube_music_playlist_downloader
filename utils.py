import json
import os
import subprocess

def create_symlink(source_file, link_name):
    try:
        os.symlink(source_file, link_name)
        print(f"Symbolic link created: {link_name} -> {source_file}")
    except FileExistsError:
        print(f"Error: The symbolic link {link_name} already exists.")
    except OSError as e:
        print(f"Error creating symbolic link: {e}")


def write_config(file, config: dict):
    with open(file, "w") as f:
        json.dump(config, f, indent=4)


def check_ffmpeg():
    ffmpeg_available = True
    try:
        subprocess.check_output(["ffmpeg", "-version"])
    except Exception as e:
        ffmpeg_available = False
    if not ffmpeg_available:
        print(
            "\n".join(
                [
                    "[ERROR] ffmpeg not found. Please ensure ffmpeg is installed",
                    "and you have included it in your PATH environment variable.",
                    "Download ffmpeg here: https://www.ffmpeg.org/download.html.",
                    "-----------------------------------------------------------",
                ]
            )
        )
    return ffmpeg_available
