#!/usr/bin/env python3
"""
Demo script showing how to use background images in both CustomTextShortEngine and CustomAudioShortEngine
"""

import os
import sys

sys.path.append(".")

from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.config.asset_db import AssetDatabase, AssetType
from shortGPT.config.languages import EDGE_TTS_VOICENAME_MAPPING, Language
from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine


def demo_background_image():
    print("🎬 Demo: Creating videos with background image instead of background video")
    print("=" * 70)

    # Check available images in the asset database
    df = AssetDatabase.get_df()
    image_assets = df[df["type"] == "image"]

    if image_assets.empty:
        print("No image assets found. Adding sample image...")
        # Add the sample image if it exists
        if os.path.exists("public/white_reddit_template.png"):
            AssetDatabase.add_local_asset(
                "sample_background_image",
                AssetType.IMAGE,
                "public/white_reddit_template.png",
            )
            print("✓ Added sample background image")
        else:
            print(
                "❌ No sample image found. Please add an image to the public folder first."
            )
            return
    else:
        print(f"Found {len(image_assets)} image asset(s):")
        for _, asset in image_assets.iterrows():
            print(f"  - {asset['name']}")

    # Check available music
    music_assets = df[df["type"] == "background music"]
    if music_assets.empty:
        print("❌ No background music found. Please add some music assets first.")
        return

    print(f"\nFound {len(music_assets)} music asset(s):")
    for _, asset in music_assets.iterrows():
        print(f"  - {asset['name']}")

    # Create voice module
    language = Language.ENGLISH
    voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]["male"])

    # Get the first available image and music
    image_name = image_assets.iloc[0]["name"]
    music_name = music_assets.iloc[0]["name"]

    print(f"\n🎯 Demo Configuration:")
    print(f"   Background Image: {image_name}")
    print(f"   Background Music: {music_name}")

    # Demo 1: CustomTextShortEngine with background image
    print(f"\n{'='*50}")
    print("📝 Demo 1: CustomTextShortEngine with Background Image")
    print(f"{'='*50}")

    try:
        # Create the engine with background image
        text_engine = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text="Welcome to ShortGPT! This video demonstrates the new background image feature "
            "using the CustomTextShortEngine. Instead of using a background video, we're using "
            "a static image that will be displayed throughout the entire video duration.",
            background_video_name="",  # No background video
            background_music_name=music_name,
            background_image_name=image_name,  # Use background image instead
            watermark="ShortGPT Text Demo",
            language=language,
        )

        print("✓ Created CustomTextShortEngine with background image")
        print("🚀 Starting video generation...")
        print("This may take a few minutes...")

        # Generate the video
        for step_num, step_info in text_engine.makeContent():
            print(f"Step {step_num}: {step_info}")

        video_path = text_engine.get_video_output_path()
        print(f"\n✅ CustomTextShortEngine video generated successfully!")
        print(f"📁 Output path: {video_path}")

    except Exception as e:
        print(f"\n❌ Error generating CustomTextShortEngine video: {e}")
        import traceback

        traceback.print_exc()

    # Demo 2: CustomAudioShortEngine with background image (if audio file exists)
    print(f"\n{'='*50}")
    print("🎵 Demo 2: CustomAudioShortEngine with Background Image")
    print(f"{'='*50}")

    # Check if sample audio exists
    sample_audio_path = "public/tinhve.wav"
    if not os.path.exists(sample_audio_path):
        print(f"❌ Sample audio file not found at {sample_audio_path}")
        print("Skipping CustomAudioShortEngine demo.")
        print("To test this feature, add an audio file to the public folder.")
    else:
        try:
            # Create the engine with background image
            audio_engine = CustomAudioShortEngine(
                voiceModule=voice_module,  # Required for compatibility but not used
                custom_audio_path=sample_audio_path,
                background_video_name="",  # No background video
                background_music_name=music_name,
                background_image_name=image_name,  # Use background image instead
                watermark="ShortGPT Audio Demo",
                language=language,
            )

            print("✓ Created CustomAudioShortEngine with background image")
            print("🚀 Starting video generation...")
            print("This may take a few minutes...")

            # Generate the video
            for step_num, step_info in audio_engine.makeContent():
                print(f"Step {step_num}: {step_info}")

            video_path = audio_engine.get_video_output_path()
            print(f"\n✅ CustomAudioShortEngine video generated successfully!")
            print(f"📁 Output path: {video_path}")

        except Exception as e:
            print(f"\n❌ Error generating CustomAudioShortEngine video: {e}")
            import traceback

            traceback.print_exc()

    print(f"\n{'='*70}")
    print("🎬 Demo Complete!")
    print(
        "You can now play the generated videos to see the background images in action!"
    )
    print("Both engines now support using static background images instead of videos.")


if __name__ == "__main__":
    demo_background_image()
