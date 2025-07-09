import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import VideoClip


def sepia_tone(clip):
    # Define sepia transformation function
    def sepia_frame(t):
        # Get frame at time t
        frame = clip.get_frame(t).astype(float)

        # Apply sepia transformation matrix
        r = 0.393 * frame[:, :, 0] + 0.769 * frame[:, :, 1] + 0.189 * frame[:, :, 2]
        g = 0.349 * frame[:, :, 0] + 0.686 * frame[:, :, 1] + 0.168 * frame[:, :, 2]
        b = 0.272 * frame[:, :, 0] + 0.534 * frame[:, :, 1] + 0.131 * frame[:, :, 2]

        # Stack RGB channels and clip values
        sepia = np.stack([r, g, b], axis=2)
        return np.clip(sepia, 0, 255).astype("uint8")

    # Create new video clip with sepia effect
    sepia_clip = VideoClip(sepia_frame, duration=clip.duration)
    sepia_clip.fps = clip.fps
    if hasattr(clip, "audio") and clip.audio:
        sepia_clip = sepia_clip.with_audio(clip.audio)

    return sepia_clip


def sepia_tone_dark(clip, darkness_factor=0.0):
    # darkness_factor: 0.0 (đen hoàn toàn) đến 1.0 (giữ nguyên độ sáng)

    def sepia_frame(t):
        frame = clip.get_frame(t).astype(float)

        # Apply sepia transformation
        r = frame[:, :, 0] + frame[:, :, 1] + frame[:, :, 2]
        g = frame[:, :, 0] + frame[:, :, 1] + frame[:, :, 2]
        b = frame[:, :, 0] + frame[:, :, 1] + frame[:, :, 2]

        sepia = np.stack([r, g, b], axis=2)

        # Apply darkness factor (reduce brightness)
        sepia_dark = sepia * darkness_factor

        return np.clip(sepia_dark, 0, 255).astype("uint8")

    sepia_clip = VideoClip(sepia_frame, duration=clip.duration)
    sepia_clip.fps = clip.fps
    if hasattr(clip, "audio") and clip.audio:
        sepia_clip = sepia_clip.with_audio(clip.audio)

    return sepia_clip


def darken_video(clip, darkness_factor=0.5):
    """
    Làm tối video bằng cách giảm độ sáng các pixel.
    darkness_factor: 0.0 (đen hoàn toàn) đến 1.0 (không thay đổi).
    """

    def darken_frame(t):
        frame = clip.get_frame(t).astype(float)
        dark_frame = frame * darkness_factor
        return np.clip(dark_frame, 0, 255).astype("uint8")

    dark_clip = VideoClip(darken_frame, duration=clip.duration)
    dark_clip.fps = clip.fps

    if hasattr(clip, "audio") and clip.audio:
        dark_clip = dark_clip.with_audio(clip.audio)

    return dark_clip


def vignette_video(clip, strength=0.6):
    h, w = clip.size[1], clip.size[0]  # height, width
    cx, cy = w / 2, h / 2

    # Đúng thứ tự height x width
    y, x = np.ogrid[:h, :w]  # <-- đây là chỗ quan trọng
    distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    max_dist = np.sqrt(cx**2 + cy**2)
    mask = 1 - strength * (distance / max_dist)
    mask = np.clip(mask, 0, 1)

    def apply_vignette(t):
        frame = clip.get_frame(t).astype(float)
        for c in range(3):
            frame[:, :, c] *= mask
        return np.clip(frame, 0, 255).astype("uint8")

    vignette_clip = VideoClip(apply_vignette, duration=clip.duration)
    vignette_clip.fps = clip.fps
    if hasattr(clip, "audio") and clip.audio:
        vignette_clip = vignette_clip.with_audio(clip.audio)

    return vignette_clip


# Load video
clip = VideoFileClip(
    "videos/2025-06-05/13-58-03 - Unleash Your Creativity with Custom Audio Content .mp4"
)

# Apply sepia
sepia_clip = vignette_video(clip, strength=1)  # Adjust strength as needed

# Export
sepia_clip.write_videofile("output_sepia.mp4", codec="libx264")
