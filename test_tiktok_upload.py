from Tiktok_uploader.Tiktok_uploader import uploadVideo

session_id = "7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d"
file = "videos/2025-06-05/13-58-03 - Unleash Your Creativity with Custom Audio Content .mp4"
title = "Test"
tags = ["Sad", "Love", "fyp"]
# schedule_time = 1672592400

# Publish the video
uploadVideo(session_id, file, title, tags, verbose=True)
# Schedule the video
# uploadVideo(session_id, file, title, tags, schedule_time, verbose=True)
