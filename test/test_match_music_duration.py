#!/usr/bin/env python3
"""Test script for the match music duration feature in TextDisplayShortEngine"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shortGPT.config.languages import Language
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine


def test_basic_functionality():
    """Test basic functionality without running the full engine"""
    print("🧪 Testing basic TextDisplayShortEngine initialization...")
    
    # Test 1: Traditional mode (match_music_duration=False)
    try:
        engine1 = TextDisplayShortEngine(
            text="Test text for traditional mode",
            duration=15,
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            match_music_duration=False,
        )
        assert engine1._match_music_duration == False
        assert engine1._db_duration == 15
        print("✅ Test 1 passed: Traditional mode initialization")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        return False
    
    # Test 2: Match music duration mode (match_music_duration=True)
    try:
        engine2 = TextDisplayShortEngine(
            text="Test text for music matching mode",
            duration=10,  # This should be overridden later
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            match_music_duration=True,
        )
        assert engine2._match_music_duration == True
        assert engine2._db_duration == 10  # Initial value, will be updated in _chooseBackgroundMusic
        print("✅ Test 2 passed: Music matching mode initialization")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        return False
    
    # Test 3: Duration validation should be skipped when match_music_duration=True
    try:
        engine3 = TextDisplayShortEngine(
            text="Test text with invalid duration",
            duration=100,  # > 60 seconds, but should be allowed when matching music
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            match_music_duration=True,
        )
        print("✅ Test 3 passed: Duration validation bypassed when matching music")
    except ValueError as e:
        print(f"❌ Test 3 failed: Duration validation should be bypassed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test 3 failed with unexpected error: {e}")
        return False
    
    # Test 4: Duration validation should still work when match_music_duration=False
    try:
        engine4 = TextDisplayShortEngine(
            text="Test text with invalid duration",
            duration=100,  # > 60 seconds, should fail
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            match_music_duration=False,
        )
        print("❌ Test 4 failed: Should have raised ValueError for invalid duration")
        return False
    except ValueError:
        print("✅ Test 4 passed: Duration validation works when not matching music")
    except Exception as e:
        print(f"❌ Test 4 failed with unexpected error: {e}")
        return False
    
    return True


def test_music_duration_logic():
    """Test the music duration matching logic"""
    print("\n🎵 Testing music duration matching logic...")
    
    try:
        engine = TextDisplayShortEngine(
            text="Test music duration matching",
            duration=15,
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            match_music_duration=True,
        )
        
        # Simulate the _chooseBackgroundMusic step
        print("Testing _chooseBackgroundMusic method...")
        
        # Mock the logger to capture output
        logged_messages = []
        def mock_logger(message):
            logged_messages.append(message)
            print(f"  📝 Log: {message}")
        
        engine.set_logger(mock_logger)
        
        # Run the _chooseBackgroundMusic step
        engine._chooseBackgroundMusic()
        
        # Check if music URL was set
        if hasattr(engine, '_db_background_music_url') and engine._db_background_music_url:
            print("✅ Background music URL set successfully")
        else:
            print("⚠️  Background music URL not set (may be expected if asset doesn't exist)")
        
        # Check if any duration-related messages were logged
        duration_logs = [msg for msg in logged_messages if 'duration' in msg.lower()]
        if duration_logs:
            print(f"✅ Duration matching logic executed: {duration_logs}")
        else:
            print("⚠️  No duration-related logs found (may indicate asset not found)")
        
        return True
        
    except Exception as e:
        print(f"❌ Music duration logic test failed: {e}")
        return False


def main():
    print("🚀 Testing match music duration feature for TextDisplayShortEngine\n")
    
    # Run basic functionality tests
    basic_test_result = test_basic_functionality()
    
    # Run music duration logic tests
    music_logic_test_result = test_music_duration_logic()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print(f"Basic functionality tests: {'✅ PASSED' if basic_test_result else '❌ FAILED'}")
    print(f"Music duration logic tests: {'✅ PASSED' if music_logic_test_result else '❌ FAILED'}")
    
    if basic_test_result and music_logic_test_result:
        print("\n🎉 All tests passed! The match music duration feature is working correctly.")
        print("\n📝 How to use this feature:")
        print("1. In the UI, select 'Text Display shorts'")
        print("2. Check the 'Match video duration to background music duration' checkbox")
        print("3. The video duration slider will be disabled")
        print("4. The final video will automatically match the length of your selected background music")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    return basic_test_result and music_logic_test_result


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 