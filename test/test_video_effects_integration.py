#!/usr/bin/env python3
"""
Test script to verify video effects integration with ShortGPT content engines.
"""


def test_video_effects_import():
    """Test that video effects module can be imported"""
    try:
        from shortGPT.editing_utils.video_effects import (
            VideoEffect,
            get_effect_parameters,
            get_video_effect_options,
        )

        print("✓ Video effects module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import video effects module: {e}")
        return False


def test_video_effect_options():
    """Test video effect options functionality"""
    try:
        from shortGPT.editing_utils.video_effects import (
            VideoEffect,
            get_effect_parameters,
            get_video_effect_options,
        )

        # Test getting effect options
        options = get_video_effect_options()
        assert len(options) > 0, "Should have video effect options"
        print(f"✓ Found {len(options)} video effect options")

        # Test effect parameters
        for name, effect in options.items():
            params = get_effect_parameters(effect)
            print(
                f"  - {name}: {effect.value} {list(params.keys()) if params else '(no params)'}"
            )

        return True
    except Exception as e:
        print(f"✗ Failed to test video effect options: {e}")
        return False


def test_editing_step_enum():
    """Test that APPLY_VIDEO_EFFECT is in EditingStep enum"""
    try:
        from shortGPT.editing_framework.editing_engine import EditingStep

        # Check if APPLY_VIDEO_EFFECT exists
        assert hasattr(
            EditingStep, "APPLY_VIDEO_EFFECT"
        ), "APPLY_VIDEO_EFFECT should be in EditingStep enum"
        print("✓ APPLY_VIDEO_EFFECT editing step found")

        # Check the value
        assert (
            EditingStep.APPLY_VIDEO_EFFECT.value == "apply_video_effect.json"
        ), "Incorrect JSON file name"
        print("✓ APPLY_VIDEO_EFFECT has correct JSON file reference")

        return True
    except Exception as e:
        print(f"✗ Failed to test EditingStep enum: {e}")
        return False


def test_json_editing_step():
    """Test that the video effect JSON file exists and has correct structure"""
    try:
        import json
        import os

        json_path = "shortGPT/editing_framework/editing_steps/apply_video_effect.json"

        # Check if file exists
        assert os.path.exists(json_path), f"JSON file should exist at {json_path}"
        print("✓ apply_video_effect.json file exists")

        # Check JSON structure
        with open(json_path, "r") as f:
            data = json.load(f)

        assert "video_effect" in data, "Should have 'video_effect' key"
        video_effect = data["video_effect"]

        assert video_effect.get("type") == "video", "Type should be 'video'"
        assert "inputs" in video_effect, "Should have 'inputs' section"
        assert "parameters" in video_effect, "Should have 'parameters' section"
        assert "actions" in video_effect, "Should have 'actions' section"

        print("✓ apply_video_effect.json has correct structure")

        return True
    except Exception as e:
        print(f"✗ Failed to test JSON editing step: {e}")
        return False


def test_content_engine_constructors():
    """Test that content engines accept video effect parameters"""
    try:
        from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
        from shortGPT.config.languages import Language
        from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine
        from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine
        from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine

        voice_module = EdgeTTSVoiceModule("en-US-AriaNeural")

        # Test CustomTextShortEngine
        engine1 = CustomTextShortEngine(
            voiceModule=voice_module,
            custom_text="Test text",
            background_video_name="test_video.mp4",
            language=Language.ENGLISH,
            video_effect="sepia_tone",
            video_effect_params={},
        )
        assert engine1._db_video_effect == "sepia_tone"
        print("✓ CustomTextShortEngine accepts video effect parameters")

        # Test TextDisplayShortEngine
        engine2 = TextDisplayShortEngine(
            text="Test display text",
            duration=10,
            background_video_name="test_video.mp4",
            language=Language.ENGLISH,
            video_effect="vignette_video",
            video_effect_params={"strength": 0.8},
        )
        assert engine2._db_video_effect == "vignette_video"
        assert engine2._db_video_effect_params == {"strength": 0.8}
        print("✓ TextDisplayShortEngine accepts video effect parameters")

        # Test CustomAudioShortEngine (without actual audio file)
        engine3 = CustomAudioShortEngine(
            voiceModule=voice_module,
            custom_audio_path="fake_audio.mp3",  # This will fail later but constructor should work
            background_video_name="test_video.mp4",
            language=Language.ENGLISH,
            video_effect="darken_video",
            video_effect_params={"darkness_factor": 0.5},
        )
        assert engine3._db_video_effect == "darken_video"
        assert engine3._db_video_effect_params == {"darkness_factor": 0.5}
        print("✓ CustomAudioShortEngine accepts video effect parameters")

        return True
    except Exception as e:
        print(f"✗ Failed to test content engine constructors: {e}")
        return False


def main():
    """Run all tests"""
    print("=== Testing Video Effects Integration ===\n")

    tests = [
        ("Import Test", test_video_effects_import),
        ("Video Effect Options Test", test_video_effect_options),
        ("Editing Step Enum Test", test_editing_step_enum),
        ("JSON Editing Step Test", test_json_editing_step),
        ("Content Engine Constructors Test", test_content_engine_constructors),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")

    print(f"\n=== Test Results: {passed}/{total} tests passed ===")

    if passed == total:
        print("🎉 All tests passed! Video effects integration is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
