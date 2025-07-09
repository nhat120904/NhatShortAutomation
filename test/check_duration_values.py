#!/usr/bin/env python3
"""Diagnostic script to check self._db_duration and music duration values"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shortGPT.config.languages import Language
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine
from shortGPT.config.asset_db import AssetDatabase


def check_duration_values():
    """Check self._db_duration and music duration values step by step"""
    print("🔍 Checking Duration Values for Match Music Duration Feature")
    print("=" * 60)
    
    # Test available music assets first
    print("\n1️⃣ CHECKING AVAILABLE MUSIC ASSETS")
    try:
        # Get all assets and filter for music
        df = AssetDatabase.get_df()
        if not df.empty:
            music_assets = df[df['type'].str.contains('music', case=False, na=False)]
            print(f"Found {len(music_assets)} music assets:")
            for idx, asset in music_assets.iterrows():
                name = asset['name']
                asset_type = asset['type']
                try:
                    duration = AssetDatabase.get_asset_duration(name)
                    print(f"  📀 {name} ({asset_type}) → {duration} seconds")
                except Exception as e:
                    print(f"  ❌ {name} ({asset_type}) → Error: {e}")
        else:
            print("❌ No assets found in database!")
            return
    except Exception as e:
        print(f"❌ Error accessing asset database: {e}")
        return
    
    # Test cases
    test_cases = [
        {
            "name": "Traditional Mode (match_music_duration=False)",
            "match_music_duration": False,
            "initial_duration": 15,
            "music_name": "Music joakim karud dreams"
        },
        {
            "name": "Match Music Duration Mode (match_music_duration=True)",
            "match_music_duration": True,
            "initial_duration": 10,
            "music_name": "Music joakim karud dreams"
        },
        {
            "name": "No Background Music (match_music_duration=True)",
            "match_music_duration": True,
            "initial_duration": 20,
            "music_name": ""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 2):
        print(f"\n{i}️⃣ TEST CASE: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Create engine
            print(f"Creating TextDisplayShortEngine with:")
            print(f"  - match_music_duration: {test_case['match_music_duration']}")
            print(f"  - initial duration: {test_case['initial_duration']} seconds")
            print(f"  - music name: '{test_case['music_name']}'")
            
            engine = TextDisplayShortEngine(
                text="Test duration values",
                duration=test_case['initial_duration'],
                background_video_name="",
                background_music_name=test_case['music_name'],
                background_image_name="white_reddit_template",
                watermark="Test",
                language=Language.ENGLISH,
                match_music_duration=test_case['match_music_duration'],
            )
            
            print(f"\n📊 INITIAL STATE:")
            print(f"  - engine._db_duration: {engine._db_duration}")
            print(f"  - engine._match_music_duration: {engine._match_music_duration}")
            print(f"  - engine._db_background_music_name: '{engine._db_background_music_name}'")
            
            # Check music duration separately
            if test_case['music_name']:
                print(f"\n🎵 CHECKING MUSIC DURATION:")
                try:
                    music_duration = AssetDatabase.get_asset_duration(test_case['music_name'])
                    print(f"  - AssetDatabase.get_asset_duration('{test_case['music_name']}'): {music_duration}")
                    print(f"  - Type: {type(music_duration)}")
                    
                    if music_duration:
                        int_duration = int(music_duration)
                        print(f"  - int(music_duration): {int_duration}")
                except Exception as e:
                    print(f"  - ❌ Error getting music duration: {e}")
            else:
                print(f"\n🎵 NO MUSIC SPECIFIED")
            
            # Run _chooseBackgroundMusic method
            print(f"\n⚙️ RUNNING _chooseBackgroundMusic():")
            engine._chooseBackgroundMusic()
            
            print(f"\n📊 FINAL STATE:")
            print(f"  - engine._db_duration: {engine._db_duration}")
            print(f"  - engine._db_background_music_url: {getattr(engine, '_db_background_music_url', 'Not set')}")
            
            # Summary
            initial_duration = test_case['initial_duration']
            final_duration = engine._db_duration
            
            if test_case['match_music_duration'] and test_case['music_name']:
                if initial_duration != final_duration:
                    print(f"✅ SUCCESS: Duration changed from {initial_duration} to {final_duration}")
                else:
                    print(f"❌ ISSUE: Duration should have changed but remained {final_duration}")
            else:
                if initial_duration == final_duration:
                    print(f"✅ SUCCESS: Duration correctly unchanged at {final_duration}")
                else:
                    print(f"⚠️ UNEXPECTED: Duration changed from {initial_duration} to {final_duration}")
                    
        except Exception as e:
            print(f"❌ ERROR in test case: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n" + "=" * 60)
    print("🏁 DURATION CHECK COMPLETE")


def check_specific_music_asset(music_name="Music joakim karud dreams"):
    """Check a specific music asset in detail"""
    print(f"\n🔍 DETAILED CHECK FOR: '{music_name}'")
    print("=" * 50)
    
    try:
        # Check if asset exists
        exists = AssetDatabase.asset_exists(music_name)
        print(f"Asset exists: {exists}")
        
        if exists:
            # Get asset link
            try:
                link = AssetDatabase.get_asset_link(music_name)
                print(f"Asset link: {link}")
            except Exception as e:
                print(f"Error getting asset link: {e}")
            
            # Get asset duration
            try:
                duration = AssetDatabase.get_asset_duration(music_name)
                print(f"Asset duration: {duration} (type: {type(duration)})")
                
                if duration:
                    print(f"Duration > 0: {duration > 0}")
                    print(f"int(duration): {int(duration)}")
                else:
                    print("Duration is None or 0")
                    
            except Exception as e:
                print(f"Error getting asset duration: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Asset does not exist!")
            
    except Exception as e:
        print(f"❌ Error checking asset: {e}")


if __name__ == "__main__":
    check_duration_values()
    check_specific_music_asset() 