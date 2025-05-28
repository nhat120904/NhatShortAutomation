#!/usr/bin/env python3
"""
Test script for CustomAudioShortEngine functionality.
This script validates that the new audio upload feature works correctly.
"""

import os
import tempfile
import shutil
from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.config.languages import Language

def create_sample_audio_file():
    """Create a sample audio file for testing"""
    # Use one of the existing audio files in the public directory
    public_audio = "/Users/nhatcuong/code_project/ShortGPT/public/tinhve.wav"
    
    if os.path.exists(public_audio):
        return public_audio
    else:
        print(f"Sample audio file not found at {public_audio}")
        print("Available files in public directory:")
        if os.path.exists("/Users/nhatcuong/code_project/ShortGPT/public"):
            for file in os.listdir("/Users/nhatcuong/code_project/ShortGPT/public"):
                if file.endswith(('.wav', '.mp3', '.m4a')):
                    print(f"  - {file}")
                    return os.path.join("/Users/nhatcuong/code_project/ShortGPT/public", file)
        return None

def test_custom_audio_engine():
    """Test the CustomAudioShortEngine initialization and basic functionality"""
    print("Testing CustomAudioShortEngine...")
    
    # Get sample audio file
    audio_file = create_sample_audio_file()
    if not audio_file:
        print("❌ No sample audio file found for testing")
        return False
    
    print(f"✅ Using audio file: {audio_file}")
    
    try:
        # Create a dummy voice module (not used for audio upload)
        voice_module = EdgeTTSVoiceModule("en-US-JennyNeural")
        
        # Initialize the CustomAudioShortEngine
        engine = CustomAudioShortEngine(
            voiceModule=voice_module,
            custom_audio_path=audio_file,
            background_video_name="minecraft_parkour_4k.mp4",  # Default background
            background_music_name="lofi.mp3",  # Default background music
            language=Language.ENGLISH,
            short_id="test_audio_short"
        )
        
        print("✅ CustomAudioShortEngine initialized successfully")
        
        # Test that the audio path is set correctly
        assert engine._db_custom_audio_path == audio_file
        print("✅ Audio path set correctly")
        
        # Test step dictionary
        expected_steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        actual_steps = list(engine.stepDict.keys())
        assert actual_steps == expected_steps
        print(f"✅ Step dictionary correct: {len(actual_steps)} steps")
        
        # Test script generation (should set placeholder)
        engine._generateScript()
        assert engine._db_script == "Custom audio content (script generated from uploaded audio)"
        print("✅ Script generation working (placeholder set)")
        
        print("\n🎉 All tests passed! CustomAudioShortEngine is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_audio_processing():
    """Test the audio processing functionality"""
    print("\nTesting audio processing...")
    
    audio_file = create_sample_audio_file()
    if not audio_file:
        return False
    
    try:
        voice_module = EdgeTTSVoiceModule("en-US-JennyNeural")
        engine = CustomAudioShortEngine(
            voiceModule=voice_module,
            custom_audio_path=audio_file,
            background_video_name="minecraft_parkour_4k.mp4",
            background_music_name="lofi.mp3",
            language=Language.ENGLISH,
            short_id="test_audio_processing"
        )
        
        # Test temp audio generation
        engine._generateTempAudio()
        assert engine._db_temp_audio_path is not None
        assert os.path.exists(engine._db_temp_audio_path)
        print("✅ Temp audio file created successfully")
        
        # Test speed up audio (should copy without modification)
        engine._speedUpAudio()
        assert engine._db_audio_path is not None
        assert os.path.exists(engine._db_audio_path)
        print("✅ Final audio file created successfully")
        
        print("🎉 Audio processing tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Audio processing test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOM AUDIO SHORT ENGINE TEST")
    print("=" * 60)
    
    success1 = test_custom_audio_engine()
    success2 = test_audio_processing()
    
    if success1 and success2:
        print("\n🎉 All tests completed successfully!")
        print("The Custom Audio Short Engine is ready to use.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
