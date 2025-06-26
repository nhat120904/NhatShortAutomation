#!/usr/bin/env python3
"""
Demo script showing how to use video effects with ShortGPT content engines.

This script demonstrates:
1. Available video effects
2. How to apply different effects to content engines
3. Effect parameters customization
"""

import os
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.config.languages import Language
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine
from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine
from shortGPT.editing_utils.video_effects import VideoEffect, get_video_effect_options, get_effect_parameters


def demo_video_effects():
    """Demonstrate video effects integration with content engines"""
    
    print("=== ShortGPT Video Effects Demo ===\n")
    
    # Show available video effects
    print("Available Video Effects:")
    effect_options = get_video_effect_options()
    for i, (name, effect) in enumerate(effect_options.items(), 1):
        params = get_effect_parameters(effect)
        param_str = f" (params: {list(params.keys())})" if params else ""
        print(f"  {i}. {name} - {effect.value}{param_str}")
    print()
    
    # Demo text for the content engines
    demo_text = "Welcome to ShortGPT! This video demonstrates amazing visual effects that can be applied to your content."
    
    # Create voice module for text-to-speech engines
    voice_module = EdgeTTSVoiceModule("en-US-AriaNeural")
    
    # Demo 1: Custom Text Engine with Sepia Effect
    print("Demo 1: Custom Text Engine with Sepia Tone Effect")
    try:
        engine1 = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text=demo_text,
            background_video_name="minecraft_parkour.mp4",  # Replace with your video asset name
            background_music_name="chill_music.mp3",       # Replace with your music asset name
            language=Language.ENGLISH,
            watermark="ShortGPT Demo",
            video_effect="sepia_tone",  # Apply sepia tone effect
            video_effect_params={}      # No additional parameters needed for sepia
        )
        print("✓ Custom Text Engine with Sepia Tone created successfully")
    except Exception as e:
        print(f"✗ Error creating Custom Text Engine: {e}")
    
    print()
    
    # Demo 2: Text Display Engine with Vignette Effect
    print("Demo 2: Text Display Engine with Vignette Effect")
    try:
        engine2 = TextDisplayShortEngine(
            text=demo_text,
            duration=15,  # 15 seconds
            background_video_name="nature_video.mp4",  # Replace with your video asset name
            background_music_name="ambient_music.mp3", # Replace with your music asset name
            language=Language.ENGLISH,
            watermark="ShortGPT Demo",
            video_effect="vignette_video",  # Apply vignette effect
            video_effect_params={"strength": 0.8}  # Stronger vignette effect
        )
        print("✓ Text Display Engine with Vignette Effect created successfully")
    except Exception as e:
        print(f"✗ Error creating Text Display Engine: {e}")
    
    print()
    
    # Demo 3: Custom Audio Engine with Dark Sepia Effect
    print("Demo 3: Custom Audio Engine with Dark Sepia Effect")
    try:
        # You would need to provide a path to an actual audio file
        audio_path = "path/to/your/audio/file.mp3"  # Replace with actual audio file path
        if os.path.exists(audio_path):
            engine3 = CustomAudioShortEngine(
                voiceModule=voice_module,
                custom_audio_path=audio_path,
                background_video_name="city_video.mp4",     # Replace with your video asset name
                background_music_name="urban_music.mp3",   # Replace with your music asset name
                language=Language.ENGLISH,
                watermark="ShortGPT Demo",
                video_effect="sepia_tone_dark",  # Apply dark sepia effect
                video_effect_params={"darkness_factor": 0.4}  # Darker effect
            )
            print("✓ Custom Audio Engine with Dark Sepia Effect created successfully")
        else:
            print("✗ Audio file not found. Please provide a valid audio file path.")
    except Exception as e:
        print(f"✗ Error creating Custom Audio Engine: {e}")
    
    print()
    
    # Demo 4: Custom Text Engine with Darken Effect
    print("Demo 4: Custom Text Engine with Darken Video Effect")
    try:
        engine4 = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text="This video uses a darkening effect to create a moody atmosphere.",
            background_video_name="landscape_video.mp4",  # Replace with your video asset name
            language=Language.ENGLISH,
            watermark="ShortGPT Demo",
            video_effect="darken_video",  # Apply darken effect
            video_effect_params={"darkness_factor": 0.6}  # 60% of original brightness
        )
        print("✓ Custom Text Engine with Darken Effect created successfully")
    except Exception as e:
        print(f"✗ Error creating Custom Text Engine: {e}")
    
    print()
    
    # Demo 5: No Effect (Default)
    print("Demo 5: Custom Text Engine without Video Effects")
    try:
        engine5 = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text="This video has no visual effects applied - showing the original video.",
            background_video_name="original_video.mp4",  # Replace with your video asset name
            language=Language.ENGLISH,
            watermark="ShortGPT Demo",
            video_effect="none",  # No effect
            video_effect_params={}
        )
        print("✓ Custom Text Engine without effects created successfully")
    except Exception as e:
        print(f"✗ Error creating Custom Text Engine: {e}")
    
    print("\n=== Demo Complete ===")
    print("\nTo actually generate videos, call the makeContent() method on any engine:")
    print("Example:")
    print("  for step, description in engine1.makeContent():")
    print("      print(f'Step {step}: {description}')")
    print("\nMake sure you have:")
    print("1. Valid background video/image assets in your asset database")
    print("2. Valid background music assets (optional)")
    print("3. Proper API keys configured if using cloud services")


def show_effect_parameters():
    """Show detailed information about effect parameters"""
    print("\n=== Video Effect Parameters Guide ===\n")
    
    effects_info = {
        VideoEffect.NONE: {
            "description": "No effect applied - original video",
            "use_case": "When you want to keep the original video quality"
        },
        VideoEffect.SEPIA_TONE: {
            "description": "Classic sepia/vintage photo effect",
            "use_case": "For nostalgic, vintage, or classic themed content"
        },
        VideoEffect.SEPIA_TONE_DARK: {
            "description": "Darker sepia effect with adjustable darkness",
            "use_case": "For dramatic, moody vintage content",
            "parameters": {
                "darkness_factor": "0.0 (black) to 1.0 (original brightness), default: 0.6"
            }
        },
        VideoEffect.DARKEN_VIDEO: {
            "description": "Reduces overall brightness of the video",
            "use_case": "For dramatic effect, highlighting text, or moody atmosphere",
            "parameters": {
                "darkness_factor": "0.0 (black) to 1.0 (original brightness), default: 0.5"
            }
        },
        VideoEffect.VIGNETTE_VIDEO: {
            "description": "Darkens the edges of the video, creating a tunnel effect",
            "use_case": "To focus attention on the center, create cinematic look",
            "parameters": {
                "strength": "0.0 (no effect) to 1.0 (maximum vignette), default: 0.6"
            }
        }
    }
    
    for effect, info in effects_info.items():
        print(f"Effect: {effect.value.upper()}")
        print(f"  Description: {info['description']}")
        print(f"  Use Case: {info['use_case']}")
        if 'parameters' in info:
            print("  Parameters:")
            for param, desc in info['parameters'].items():
                print(f"    - {param}: {desc}")
        print()


if __name__ == "__main__":
    demo_video_effects()
    show_effect_parameters()
    
    print("\n" + "="*50)
    print("Video Effects successfully integrated with ShortGPT!")
    print("You can now apply visual effects to all content engines.")
    print("="*50) 