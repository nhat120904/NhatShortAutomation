#!/usr/bin/env python3
"""Debug script to trace UI parameter passing"""

def debug_ui_parameters():
    """Print the exact parameter order expected by UI functions"""
    
    print("🔍 UI Parameter Order Debug")
    print("=" * 50)
    
    print("\n📝 create_short() parameters (in order):")
    create_short_params = [
        "numShorts",
        "short_type", 
        "tts_engine",
        "language_eleven",
        "language_edge",
        "numImages",
        "watermark",
        "background_video_list",     # 8
        "background_music_list",     # 9
        "background_image_list",     # 10
        "background_type",           # 11
        "facts_subject",             # 12
        "voice_eleven",              # 13
        "custom_text",               # 14
        "custom_audio",              # 15
        "display_text",              # 16
        "video_duration",            # 17
        "match_music_duration",      # 18 ← This should be position 18
        "video_effect",              # 19
        "darkness_factor",           # 20
        "vignette_strength",         # 21
        "progress"
    ]
    
    for i, param in enumerate(create_short_params):
        marker = " ← TARGET" if param == "match_music_duration" else ""
        print(f"  {i+1:2d}. {param}{marker}")
    
    print(f"\n📝 createButton.click() inputs order:")
    click_inputs = [
        "numShorts",                     # 1
        "short_type",                    # 2  
        "tts_engine",                    # 3
        "language_eleven",               # 4
        "language_edge",                 # 5
        "numImages",                     # 6
        "watermark",                     # 7
        "background_video_checkbox()",   # 8
        "background_music_checkbox()",   # 9
        "background_image_checkbox()",   # 10
        "background_type",               # 11
        "facts_subject",                 # 12
        "voice_eleven",                  # 13
        "custom_text",                   # 14
        "custom_audio",                  # 15
        "display_text",                  # 16
        "video_duration",                # 17
        "match_music_duration",          # 18 ← This should match position 18
        "video_effect",                  # 19
        "darkness_factor",               # 20
        "vignette_strength"              # 21
    ]
    
    for i, param in enumerate(click_inputs):
        marker = " ← TARGET" if param == "match_music_duration" else ""
        print(f"  {i+1:2d}. {param}{marker}")
    
    print(f"\n🔍 Parameter Position Check:")
    match_music_create_short_pos = create_short_params.index("match_music_duration") + 1
    match_music_click_pos = click_inputs.index("match_music_duration") + 1
    
    print(f"  match_music_duration in create_short(): position {match_music_create_short_pos}")
    print(f"  match_music_duration in click inputs: position {match_music_click_pos}")
    
    if match_music_create_short_pos == match_music_click_pos:
        print("  ✅ Positions match - parameter order is correct!")
    else:
        print("  ❌ Position mismatch - this could cause parameter confusion!")
    
    print(f"\n💡 Quick UI Test Instructions:")
    print("1. Start UI with: python runShortGPT.py")
    print("2. Select 'Text Display shorts'")
    print("3. Check the checkbox appears")
    print("4. Click the checkbox - watch for: 'DEBUG UI: Checkbox changed to: True'")
    print("5. Fill form and click 'Create Shorts'")
    print("6. Watch for: 'DEBUG UI: create_short called with match_music_duration = True'")


if __name__ == "__main__":
    debug_ui_parameters() 