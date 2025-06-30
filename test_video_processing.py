#!/usr/bin/env python3
"""
Test script to verify video processing improvements in CoreEditingEngine
"""

import os
import tempfile

from shortGPT.editing_framework.core_editing_engine import (
    CoreEditingEngine,
    validate_media_file,
)


def test_empty_file_handling():
    """Test handling of empty video files"""
    print("Testing empty file handling...")

    # Create an empty file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        empty_file = tmp.name

    try:
        validate_media_file(empty_file, "video")
        print("❌ Should have failed for empty file")
        return False
    except ValueError as e:
        if "empty" in str(e).lower():
            print("✅ Correctly detected empty file")
            return True
        else:
            print(f"❌ Wrong error for empty file: {e}")
            return False
    finally:
        os.unlink(empty_file)


def test_nonexistent_file_handling():
    """Test handling of non-existent files"""
    print("Testing non-existent file handling...")

    fake_file = "/tmp/nonexistent_video.mp4"

    try:
        validate_media_file(fake_file, "video")
        print("❌ Should have failed for non-existent file")
        return False
    except FileNotFoundError as e:
        print("✅ Correctly detected non-existent file")
        return True
    except Exception as e:
        print(f"❌ Wrong error type for non-existent file: {e}")
        return False


def test_video_asset_processing():
    """Test video asset processing with error handling"""
    print("Testing video asset processing...")

    engine = CoreEditingEngine()

    # Test with non-existent file
    asset = {"parameters": {"url": "/tmp/nonexistent_video.mp4"}, "actions": []}

    try:
        engine.process_video_asset(asset)
        print("❌ Should have failed for non-existent video")
        return False
    except Exception as e:
        if "not found" in str(e).lower() or "failed to load" in str(e).lower():
            print("✅ Correctly handled non-existent video asset")
            return True
        else:
            print(f"❌ Unexpected error: {e}")
            return False


def main():
    """Run all tests"""
    print("Running video processing tests...\n")

    tests = [
        test_empty_file_handling,
        test_nonexistent_file_handling,
        test_video_asset_processing,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}\n")

    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print(
            "🎉 All tests passed! The video processing improvements are working correctly."
        )
    else:
        print("⚠️  Some tests failed. There may be issues with the improvements.")


if __name__ == "__main__":
    main()
