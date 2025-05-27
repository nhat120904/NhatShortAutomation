#!/usr/bin/env python3
"""
Utility script to clean up problematic m3u8 files that cause MoviePy errors
"""

import os
import glob

def find_m3u8_files():
    """Find all m3u8 files in temp directories"""
    m3u8_files = []
    for pattern in ['temp_videos/*.m3u8', 'temp_images/*.m3u8', '.editing_assets/**/*.m3u8']:
        m3u8_files.extend(glob.glob(pattern, recursive=True))
    return m3u8_files

def cleanup_m3u8_files():
    """Remove all m3u8 files from temp directories"""
    m3u8_files = find_m3u8_files()
    
    if not m3u8_files:
        print("No m3u8 files found.")
        return
    
    print(f"Found {len(m3u8_files)} m3u8 files:")
    for file in m3u8_files:
        print(f"  - {file}")
    
    response = input("\nDo you want to delete these m3u8 files? (y/N): ")
    if response.lower() == 'y':
        deleted_count = 0
        for file in m3u8_files:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
        
        print(f"\nDeleted {deleted_count} out of {len(m3u8_files)} files.")
    else:
        print("No files deleted.")

def check_format_settings():
    """Check if the format settings in handle_videos.py are correct"""
    try:
        with open('shortGPT/editing_utils/handle_videos.py', 'r') as f:
            content = f.read()
            if 'bestvideo[ext=mp4]' in content and 'bestvideo[ext=m3u8]' in content:
                print("✅ Format settings are correct - MP4 preferred, M3U8 supported as fallback")
            elif 'bestvideo[ext=mp4]' in content:
                print("✅ Format settings prioritize MP4 format")
            elif 'bestvideo[ext=m3u8]' in content:
                print("⚠️  Format settings include M3U8 - ensure conversion is implemented")
            else:
                print("⚠️  Could not determine format settings")
    except FileNotFoundError:
        print("❌ Could not find handle_videos.py file")

if __name__ == "__main__":
    print("M3U8 Cleanup Utility")
    print("=" * 30)
    
    print("\n1. Checking format settings...")
    check_format_settings()
    
    print("\n2. Scanning for m3u8 files...")
    cleanup_m3u8_files()
    
    print("\nDone!") 