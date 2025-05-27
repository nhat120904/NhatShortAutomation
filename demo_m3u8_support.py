#!/usr/bin/env python3
"""
Demo script showing how M3U8 files are now supported through automatic conversion to MP4
"""

import os
import sys
sys.path.append('.')

def demo_m3u8_workflow():
    """Demonstrate the M3U8 to MP4 workflow"""
    
    print("ShortGPT M3U8 Support Demo")
    print("=" * 50)
    print()
    
    print("📋 NEW WORKFLOW:")
    print("1. yt-dlp downloads video URLs (may include M3U8 playlists)")
    print("2. If an M3U8 file is detected, it's automatically converted to MP4 using FFmpeg")
    print("3. The converted MP4 file is used with MoviePy for video processing")
    print("4. All existing ShortGPT functionality works seamlessly")
    print()
    
    print("🔧 TECHNICAL DETAILS:")
    print("- Format preference: MP4 > WebM > Other formats > M3U8 (as fallback)")
    print("- Conversion uses: ffmpeg -i input.m3u8 -c copy output.mp4")
    print("- Converted files are cached in temp_videos/ directory")
    print("- Absolute paths are used to prevent directory change issues")
    print()
    
    print("✅ BENEFITS:")
    print("- Support for streaming video sources that only provide M3U8")
    print("- Automatic conversion - no manual intervention needed")
    print("- Fast conversion using stream copy (no re-encoding)")
    print("- Compatible with all existing ShortGPT engines")
    print()
    
    print("📁 FILE LOCATIONS:")
    print("- Source code: shortGPT/editing_framework/core_editing_engine.py")
    print("- Format settings: shortGPT/editing_utils/handle_videos.py")
    print("- Converted files: temp_videos/converted_*.mp4")
    print()
    
    # Check current setup
    print("🔍 CURRENT SETUP:")
    
    # Check ffmpeg
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        ffmpeg_version = result.stdout.split('\n')[0]
        print(f"✅ {ffmpeg_version}")
    except FileNotFoundError:
        print("❌ FFmpeg not found - M3U8 conversion will not work")
    
    # Check format settings
    try:
        with open('shortGPT/editing_utils/handle_videos.py', 'r') as f:
            content = f.read()
            if 'bestvideo[ext=m3u8]' in content:
                print("✅ M3U8 format support enabled in yt-dlp settings")
            else:
                print("❌ M3U8 format support not found in yt-dlp settings")
    except FileNotFoundError:
        print("❌ Could not check format settings")
    
    # Check conversion method
    try:
        from shortGPT.editing_framework.core_editing_engine import CoreEditingEngine
        engine = CoreEditingEngine()
        if hasattr(engine, '_convert_m3u8_to_mp4'):
            print("✅ M3U8 to MP4 conversion method available")
        else:
            print("❌ M3U8 conversion method not found")
    except Exception as e:
        print(f"❌ Could not load CoreEditingEngine: {e}")
    
    print()
    print("🎬 USAGE:")
    print("Simply use ShortGPT as normal! M3U8 files will be automatically")
    print("converted to MP4 behind the scenes when encountered.")

if __name__ == "__main__":
    demo_m3u8_workflow() 