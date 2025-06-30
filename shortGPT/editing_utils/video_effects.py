from enum import Enum

import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import VideoClip


class VideoEffect(Enum):
    """Enumeration of available video effects"""

    NONE = "none"
    SEPIA_TONE = "sepia_tone"
    SEPIA_TONE_DARK = "sepia_tone_dark"
    DARKEN_VIDEO = "darken_video"
    VIGNETTE_VIDEO = "vignette_video"


def sepia_tone(clip):
    """
    Apply sepia tone effect to video clip
    """

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


def sepia_tone_dark(clip, darkness_factor=0.6):
    """
    Apply dark sepia tone effect to video clip
    darkness_factor: 0.0 (completely black) to 1.0 (original brightness)
    """

    def sepia_frame(t):
        frame = clip.get_frame(t).astype(float)

        # Apply sepia transformation
        r = 0.393 * frame[:, :, 0] + 0.769 * frame[:, :, 1] + 0.189 * frame[:, :, 2]
        g = 0.349 * frame[:, :, 0] + 0.686 * frame[:, :, 1] + 0.168 * frame[:, :, 2]
        b = 0.272 * frame[:, :, 0] + 0.534 * frame[:, :, 1] + 0.131 * frame[:, :, 2]

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
    Darken video by reducing pixel brightness
    darkness_factor: 0.0 (completely black) to 1.0 (no change)
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
    """
    Apply vignette effect to video clip
    strength: 0.0 (no effect) to 1.0 (maximum vignette effect)
    """
    h, w = clip.size[1], clip.size[0]  # height, width
    cx, cy = w / 2, h / 2

    # Create distance mask with correct height x width order
    y, x = np.ogrid[:h, :w]
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


def apply_video_effect(clip, effect: VideoEffect, **kwargs):
    """
    Apply video effect to clip based on effect type

    Args:
        clip: MoviePy VideoClip
        effect: VideoEffect enum value
        **kwargs: Additional parameters for specific effects

    Returns:
        Modified VideoClip with effect applied
    """
    if effect == VideoEffect.NONE:
        return clip
    elif effect == VideoEffect.SEPIA_TONE:
        return sepia_tone(clip)
    elif effect == VideoEffect.SEPIA_TONE_DARK:
        darkness_factor = kwargs.get("darkness_factor", 0.6)
        return sepia_tone_dark(clip, darkness_factor)
    elif effect == VideoEffect.DARKEN_VIDEO:
        darkness_factor = kwargs.get("darkness_factor", 0.5)
        return darken_video(clip, darkness_factor)
    elif effect == VideoEffect.VIGNETTE_VIDEO:
        strength = kwargs.get("strength", 0.6)
        return vignette_video(clip, strength)
    else:
        raise ValueError(f"Unsupported video effect: {effect}")


def apply_video_effect_to_file(
    input_path: str, output_path: str, effect: VideoEffect, **kwargs
):
    """
    Apply video effect to a video file and save to output path

    Args:
        input_path: Path to input video file
        output_path: Path to save output video file
        effect: VideoEffect enum value
        **kwargs: Additional parameters for specific effects
    """
    clip = VideoFileClip(input_path)

    # Apply the effect
    effect_clip = apply_video_effect(clip, effect, **kwargs)

    # Write the output
    effect_clip.write_videofile(output_path, codec="libx264")

    # Clean up
    clip.close()
    effect_clip.close()


def get_video_effect_options():
    """
    Get available video effect options for UI selection

    Returns:
        Dict mapping effect names to their enum values
    """
    return {
        "None": VideoEffect.NONE,
        "Sepia Tone": VideoEffect.SEPIA_TONE,
        "Dark Sepia Tone": VideoEffect.SEPIA_TONE_DARK,
        "Darken Video": VideoEffect.DARKEN_VIDEO,
        "Vignette Effect": VideoEffect.VIGNETTE_VIDEO,
    }


def get_effect_parameters(effect: VideoEffect):
    """
    Get the adjustable parameters for a given effect

    Returns:
        Dict with parameter names and their default values
    """
    if effect == VideoEffect.SEPIA_TONE_DARK:
        return {"darkness_factor": 0.6}
    elif effect == VideoEffect.DARKEN_VIDEO:
        return {"darkness_factor": 0.5}
    elif effect == VideoEffect.VIGNETTE_VIDEO:
        return {"strength": 0.6}
    else:
        return {}
