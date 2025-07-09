#!/usr/bin/env python3
"""
Test script for the CustomTextShortEngine
"""

from shortGPT.audio.edge_voice_module import (
    EDGE_TTS_VOICENAME_MAPPING,
    EdgeTTSVoiceModule,
)
from shortGPT.config.languages import Language
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine


def test_custom_text_engine():
    """Test the CustomTextShortEngine with sample data"""

    # Sample custom text
    custom_text = """
    Welcome to our amazing custom video! This is a test of the custom text feature. 
    Instead of using AI to generate content, you can now write your own script.
    This text will be converted to speech and displayed throughout the entire video.
    Perfect for when you want full control over your content!
    """

    try:
        # Initialize voice module (using EdgeTTS for free voice synthesis)
        voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.ENGLISH]["male"]
        voice_module = EdgeTTSVoiceModule(voice_name)

        # Create the custom text engine
        engine = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text=custom_text,
            background_video_name="test_video",  # This would normally be a real video asset
            background_music_name="test_music",  # This would normally be a real music asset
            num_images=5,
            watermark="CustomTest",
            language=Language.ENGLISH,
        )

        # Test the script generation
        engine._generateScript()

        print("✅ CustomTextShortEngine test passed!")
        print(f"Generated script: {engine._db_script[:100]}...")

        return True

    except Exception as e:
        print(f"❌ CustomTextShortEngine test failed: {e}")
        return False


def test_empty_text():
    """Test that empty text raises appropriate error"""

    try:
        voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.ENGLISH]["male"]
        voice_module = EdgeTTSVoiceModule(voice_name)

        engine = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text="",  # Empty text should cause error
            background_video_name="test_video",
            background_music_name="test_music",
        )

        # This should raise an error
        engine._generateScript()

        print("❌ Empty text test failed - should have raised an error!")
        return False

    except ValueError as e:
        print("✅ Empty text validation test passed!")
        return True
    except Exception as e:
        print(f"❌ Unexpected error in empty text test: {e}")
        return False


if __name__ == "__main__":
    print("Testing CustomTextShortEngine...")

    # Run tests
    test1_passed = test_custom_text_engine()
    test2_passed = test_empty_text()

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The CustomTextShortEngine is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the implementation.")
