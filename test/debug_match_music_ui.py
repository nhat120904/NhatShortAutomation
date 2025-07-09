#!/usr/bin/env python3
"""Debug script to test match music duration feature manually"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shortGPT.config.languages import Language
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine


def test_manual_match_music_duration():
    """Test the feature manually with explicit parameters"""
    print("🔍 Manual Test: Testing match music duration feature")
    
    print("\n=== Test 1: Manual False (traditional mode) ===")
    try:
        engine1 = TextDisplayShortEngine(
            text="Test text with traditional duration",
            duration=15,
            background_video_name="",
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            watermark="Test",
            language=Language.ENGLISH,
            match_music_duration=False,  # Explicitly False
        )
        
        print(f"Engine created with _match_music_duration = {engine1._match_music_duration}")
        print(f"Initial duration = {engine1._db_duration}")
        
        # Test the _chooseBackgroundMusic method directly
        print("\nTesting _chooseBackgroundMusic method...")
        engine1._chooseBackgroundMusic()
        
        print(f"Final duration after _chooseBackgroundMusic = {engine1._db_duration}")
        print("✅ Test 1 completed")
        
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test 2: Manual True (match music duration mode) ===")
    try:
        engine2 = TextDisplayShortEngine(
            text="Test text with music-matched duration",
            duration=10,  # This should be overridden
            background_video_name="",
            background_music_name="Music joakim karud dreams",
            background_image_name="white_reddit_template",
            watermark="Test",
            language=Language.ENGLISH,
            match_music_duration=True,  # Explicitly True
        )
        
        print(f"Engine created with _match_music_duration = {engine2._match_music_duration}")
        print(f"Initial duration = {engine2._db_duration}")
        
        # Test the _chooseBackgroundMusic method directly
        print("\nTesting _chooseBackgroundMusic method...")
        engine2._chooseBackgroundMusic()
        
        print(f"Final duration after _chooseBackgroundMusic = {engine2._db_duration}")
        print("✅ Test 2 completed")
        
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== Test 3: Check available music assets ===")
    try:
        from shortGPT.config.asset_db import AssetDatabase
        
        # Check if the music asset exists
        music_name = "Music joakim karud dreams"
        print(f"Checking if music asset '{music_name}' exists...")
        
        if AssetDatabase.asset_exists(music_name):
            print(f"✅ Music asset '{music_name}' exists")
            try:
                duration = AssetDatabase.get_asset_duration(music_name)
                print(f"✅ Music duration: {duration} seconds")
            except Exception as e:
                print(f"❌ Error getting music duration: {e}")
        else:
            print(f"❌ Music asset '{music_name}' does not exist")
            print("Available assets:")
            df = AssetDatabase.get_df()
            if not df.empty:
                print(df.to_string())
            else:
                print("No assets found in database")
                
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_manual_match_music_duration() 