#!/usr/bin/env python3
"""
Test script to verify m3u8 to mp4 conversion functionality
"""

import os
import sys

sys.path.append(".")

from shortGPT.editing_framework.core_editing_engine import CoreEditingEngine


def test_m3u8_conversion():
    """Test the m3u8 to mp4 conversion functionality"""

    print("Testing M3U8 to MP4 Conversion")
    print("=" * 40)

    # Create an instance of CoreEditingEngine
    engine = CoreEditingEngine()

    # Test with a sample m3u8 URL (this is a common test URL format)
    test_m3u8_url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"

    print(f"Testing conversion of: {test_m3u8_url}")

    try:
        # Test the conversion
        converted_path = engine._convert_m3u8_to_mp4(test_m3u8_url)

        if os.path.exists(converted_path):
            file_size = os.path.getsize(converted_path)
            print(f"✅ Conversion successful!")
            print(f"   Output file: {converted_path}")
            print(f"   File size: {file_size:,} bytes")

            # Test if MoviePy can load the converted file
            try:
                from moviepy import VideoFileClip

                with VideoFileClip(converted_path) as clip:
                    print(f"   Duration: {clip.duration:.2f} seconds")
                    print(f"   Resolution: {clip.w}x{clip.h}")
                    print("✅ MoviePy can successfully load the converted file!")

            except Exception as e:
                print(f"❌ MoviePy failed to load converted file: {e}")
                return False

        else:
            print("❌ Conversion failed - output file not found")
            return False

    except Exception as e:
        print(f"❌ Conversion failed with error: {e}")
        return False

    return True


def test_local_m3u8():
    """Test with a local m3u8 file if available"""

    # Check if there's a local m3u8 file to test with
    local_m3u8_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".m3u8"):
                local_m3u8_files.append(os.path.join(root, file))

    if local_m3u8_files:
        print(f"\nTesting with local m3u8 file: {local_m3u8_files[0]}")

        engine = CoreEditingEngine()
        try:
            converted_path = engine._convert_m3u8_to_mp4(local_m3u8_files[0])
            print(f"✅ Local file conversion successful: {converted_path}")
            return True
        except Exception as e:
            print(f"❌ Local file conversion failed: {e}")
            return False
    else:
        print("\nNo local m3u8 files found for testing")
        return True


if __name__ == "__main__":
    print("M3U8 to MP4 Conversion Test")
    print("=" * 50)

    # Check if ffmpeg is available
    import subprocess

    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found. Please install FFmpeg to use m3u8 conversion.")
        sys.exit(1)

    print("\n1. Testing URL-based m3u8 conversion...")
    url_test_result = test_m3u8_conversion()

    print("\n2. Testing local m3u8 conversion...")
    local_test_result = test_local_m3u8()

    print("\nTest Results:")
    print(f"URL conversion: {'✅ PASS' if url_test_result else '❌ FAIL'}")
    print(f"Local conversion: {'✅ PASS' if local_test_result else '❌ FAIL'}")

    if url_test_result and local_test_result:
        print("\n🎉 All tests passed! M3U8 to MP4 conversion is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
