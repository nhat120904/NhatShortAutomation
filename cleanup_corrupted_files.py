#!/usr/bin/env python3
"""
Utility script to detect and clean up corrupted video files in ShortGPT editing assets.
This script will scan for video files with invalid duration or other corruption issues.
"""

import os
import sys

from moviepy import VideoFileClip


def check_video_file(file_path):
    """Check if a video file is corrupted"""
    try:
        if not os.path.exists(file_path):
            return False, "File not found"

        if os.path.getsize(file_path) == 0:
            return False, "File is empty"

        # Try to load with MoviePy
        clip = VideoFileClip(file_path)
        if clip.duration is None or clip.duration <= 0:
            clip.close()
            return False, "Invalid duration"

        clip.close()
        return True, "OK"

    except Exception as e:
        return False, f"Error: {str(e)}"


def scan_directory(directory):
    """Scan directory for video files and check them"""
    corrupted_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".mp4", ".avi", ".mov", ".mkv", ".webm")):
                file_path = os.path.join(root, file)
                is_valid, reason = check_video_file(file_path)

                if not is_valid:
                    print(f"CORRUPTED: {file_path} - {reason}")
                    corrupted_files.append((file_path, reason))
                else:
                    print(f"OK: {file_path}")

    return corrupted_files


def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = ".editing_assets"

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist")
        return

    print(f"Scanning {directory} for corrupted video files...")
    corrupted_files = scan_directory(directory)

    if corrupted_files:
        print(f"\nFound {len(corrupted_files)} corrupted files:")
        for file_path, reason in corrupted_files:
            print(f"  {file_path} - {reason}")

        response = input("\nDo you want to delete these corrupted files? (y/N): ")
        if response.lower() == "y":
            for file_path, reason in corrupted_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
    else:
        print("No corrupted files found!")


if __name__ == "__main__":
    main()
