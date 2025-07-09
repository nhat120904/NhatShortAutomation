#!/usr/bin/env python3
"""
Demo script showing how to use the CustomTextShortEngine
This allows users to input their own text instead of relying on LLM generation
"""

from shortGPT.audio.edge_voice_module import (
    EDGE_TTS_VOICENAME_MAPPING,
    EdgeTTSVoiceModule,
)
from shortGPT.config.asset_db import AssetDatabase, AssetType
from shortGPT.config.languages import Language
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine


def setup_assets():
    """Set up sample assets for the demo"""
    print("Setting up demo assets...")

    # Note: In a real scenario, you would add actual video and music assets
    # For demo purposes, we're showing how to set them up
    try:
        # Add sample background video (you would replace with real video URL)
        AssetDatabase.add_remote_asset(
            "demo_background",
            AssetType.BACKGROUND_VIDEO,
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Replace with actual video
        )

        # Add sample background music (you would replace with real music URL)
        AssetDatabase.add_remote_asset(
            "demo_music",
            AssetType.BACKGROUND_MUSIC,
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Replace with actual music
        )

        print("✅ Assets set up successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Asset setup failed: {e}")
        print(
            "This is expected in demo mode - you would need real assets for actual video generation"
        )
        return False


def demo_custom_text_video():
    """Demonstrate creating a video with custom text"""

    print("🎬 Creating a custom text video...")

    # Your custom text - this will be the entire content of the video
    custom_text = """
    Hello everyone! Welcome to our channel. 
    
    Today I want to share some amazing facts about technology.
    
    Did you know that the first computer was invented in 1943? It was called ENIAC and it weighed 30 tons!
    
    Another fascinating fact: The internet was originally created as a military project called ARPANET in 1969.
    
    Technology has come such a long way since then. From room-sized computers to smartphones that fit in our pockets.
    
    Thanks for watching, and don't forget to subscribe for more amazing content!
    """

    try:
        # Set up voice module (using free EdgeTTS)
        voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.ENGLISH]["male"]
        voice_module = EdgeTTSVoiceModule(voice_name)

        # Create the custom text engine
        engine = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text=custom_text,
            background_video_name="demo_background",
            background_music_name="demo_music",
            num_images=5,  # Add 5 relevant images
            watermark="MyChannel",  # Your channel watermark
            language=Language.ENGLISH,
        )

        print("✅ Engine created successfully!")
        print(f"📝 Script length: {len(custom_text)} characters")
        print(f"🎯 Script preview: {custom_text[:100]}...")

        # In a real scenario, you would call this to generate the video:
        # for step_num, step_info in engine.makeContent():
        #     print(f"Step {step_num}: {step_info}")
        # print(f"🎉 Video saved to: {engine.get_video_output_path()}")

        print("\n💡 To actually generate the video, you would:")
        print("1. Set up real background video and music assets")
        print("2. Configure your API keys if needed")
        print("3. Call engine.makeContent() to generate the video")

        return True

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def main():
    print("🚀 CustomTextShortEngine Demo")
    print("=" * 50)
    print("This demo shows how to create videos with custom text content")
    print("instead of relying on AI-generated content.\n")

    # Set up assets
    setup_assets()
    print()

    # Demo the custom text feature
    demo_custom_text_video()

    print("\n" + "=" * 50)
    print("✨ Demo completed!")
    print("\nHow to use in the GUI:")
    print("1. Run the ShortGPT application")
    print("2. Select 'Custom Text shorts' from the dropdown")
    print("3. Enter your custom text in the text area")
    print("4. Configure other settings (voice, background, etc.)")
    print("5. Click 'Create Shorts' to generate your video!")


if __name__ == "__main__":
    main()
