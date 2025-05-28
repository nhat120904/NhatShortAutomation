#!/usr/bin/env python3
"""
Demo script showing how to use the new Custom Audio Short Engine.
This demonstrates the programmatic usage of the CustomAudioShortEngine.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, '/Users/nhatcuong/code_project/ShortGPT')

def demo_usage():
    """Demonstrate how to use the CustomAudioShortEngine"""
    
    print("=" * 60)
    print("CUSTOM AUDIO SHORT ENGINE - USAGE DEMO")
    print("=" * 60)
    
    print("\n1. 📂 PREPARING AUDIO FILE")
    print("   - Supported formats: MP3, WAV, M4A, AAC, FLAC, OGG")
    print("   - Recommended: Clear speech, good quality")
    print("   - Duration: Ideally under 60 seconds for shorts")
    
    # Check for sample audio
    sample_audio = "/Users/nhatcuong/code_project/ShortGPT/public/tinhve.wav"
    if os.path.exists(sample_audio):
        print(f"   ✅ Sample audio found: {sample_audio}")
    else:
        print("   ⚠️  No sample audio found, you'll need to provide your own")
    
    print("\n2. 🖥️  USING THE UI")
    print("   a. Start ShortGPT: python runShortGPT.py")
    print("   b. Go to 'Short Automation' tab")
    print("   c. Select 'Custom Audio shorts' from dropdown")
    print("   d. Upload your audio file")
    print("   e. Configure background video and music")
    print("   f. Click 'Create Shorts'")
    
    print("\n3. 🔧 PROGRAMMATIC USAGE")
    print("   ```python")
    print("   from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine")
    print("   from shortGPT.config.languages import Language")
    print("   ")
    print("   engine = CustomAudioShortEngine(")
    print("       voiceModule=None,  # Not needed for audio upload")
    print("       custom_audio_path='/path/to/your/audio.mp3',")
    print("       background_video_name='minecraft_parkour_4k.mp4',")
    print("       background_music_name='lofi.mp3',")
    print("       language=Language.ENGLISH,")
    print("       num_images=10,")
    print("       watermark='Your Channel'")
    print("   )")
    print("   ")
    print("   # Generate the short video")
    print("   for step_num, step_info in engine.makeContent():")
    print("       print(f'Step {step_num}: {step_info}')")
    print("   ")
    print("   video_path = engine.get_video_output_path()")
    print("   ```")
    
    print("\n4. 🎯 KEY ADVANTAGES")
    advantages = [
        "No TTS API keys required",
        "Use professional voice recordings",
        "Faster processing (skip script + TTS generation)",
        "Support for multiple audio formats",
        "Same video automation features",
        "Automatic audio format conversion"
    ]
    
    for i, advantage in enumerate(advantages, 1):
        print(f"   {i}. {advantage}")
    
    print("\n5. 📋 WORKFLOW COMPARISON")
    print("\n   BEFORE (Custom Text Shorts):")
    print("   Text → TTS API → Audio → Video + Captions → Final Video")
    print("   Steps: 12 (includes script generation and TTS)")
    print("\n   AFTER (Custom Audio Shorts):")
    print("   Audio File → Video + Captions → Final Video")
    print("   Steps: 10 (skips script generation and TTS)")
    
    print("\n6. 🚀 GETTING STARTED")
    print("   1. Prepare your audio file (clear speech, good quality)")
    print("   2. Run: python runShortGPT.py")
    print("   3. Select 'Custom Audio shorts'")
    print("   4. Upload your audio and configure settings")
    print("   5. Create your short!")
    
    print("\n" + "=" * 60)
    print("Ready to create shorts with your own audio! 🎉")
    print("=" * 60)

if __name__ == "__main__":
    demo_usage()
