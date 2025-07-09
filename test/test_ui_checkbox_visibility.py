#!/usr/bin/env python3
"""Test script to check checkbox visibility logic"""

def test_checkbox_visibility():
    """Test the visibility logic for match_music_duration checkbox"""
    
    print("🔍 Testing checkbox visibility logic")
    
    # Simulate the on_short_type_change function
    def on_short_type_change(x):
        return (
            x == "Custom Facts shorts",    # facts_subject visible
            x == "Custom Text shorts",     # custom_text visible  
            x == "Custom Audio shorts",    # custom_audio visible
            x == "Text Display shorts",    # display_text visible
            x == "Text Display shorts",    # video_duration visible
            x == "Text Display shorts",    # match_music_duration visible
        )
    
    # Test different short types
    test_cases = [
        "Reddit Story shorts",
        "Custom Text shorts", 
        "Custom Audio shorts",
        "Text Display shorts",
        "Custom Facts shorts"
    ]
    
    for short_type in test_cases:
        results = on_short_type_change(short_type)
        match_music_visible = results[5]  # match_music_duration is the 6th element (index 5)
        
        print(f"Short type: '{short_type}' -> match_music_duration visible: {match_music_visible}")
        
        if short_type == "Text Display shorts" and not match_music_visible:
            print("❌ ERROR: match_music_duration should be visible for Text Display shorts!")
            return False
        elif short_type != "Text Display shorts" and match_music_visible:
            print(f"❌ ERROR: match_music_duration should NOT be visible for {short_type}!")
            return False
    
    print("✅ Checkbox visibility logic is correct!")
    return True

if __name__ == "__main__":
    test_checkbox_visibility() 