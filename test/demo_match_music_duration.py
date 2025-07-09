from shortGPT.config.languages import Language
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine


def main():
    print("Testing TextDisplayShortEngine with match_music_duration feature")
    
    # Example 1: Traditional fixed duration (15 seconds)
    print("\n=== Example 1: Fixed Duration (15 seconds) ===")
    engine1 = TextDisplayShortEngine(
        text="Welcome to our channel! This video has a fixed 15-second duration.",
        duration=15,
        background_video_name="",  # Using background image instead
        background_music_name="Music joakim karud dreams",  # Background music from template
        background_image_name="white_reddit_template",  # Background image from template
        watermark="Your Channel Name",
        language=Language.ENGLISH,
        match_music_duration=False,  # Traditional mode
    )
    
    try:
        print("Creating video with fixed 15-second duration...")
        for step_num, step_info in engine1.makeContent():
            print(f"Step {step_num}: {step_info}")
        print(f"✅ Video created successfully at: {engine1._db_video_path}")
        print(f"Final video duration: {engine1._db_duration} seconds")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Match music duration
    print("\n=== Example 2: Match Music Duration ===")
    engine2 = TextDisplayShortEngine(
        text="This video duration will automatically match the background music length!",
        duration=10,  # This will be overridden by music duration
        background_video_name="",
        background_music_name="Music joakim karud dreams",  # This will determine the actual duration
        background_image_name="white_reddit_template",
        watermark="Auto Duration Demo",
        language=Language.ENGLISH,
        match_music_duration=True,  # NEW FEATURE!
    )
    
    try:
        print("Creating video with automatic music-matched duration...")
        for step_num, step_info in engine2.makeContent():
            print(f"Step {step_num}: {step_info}")
        print(f"✅ Video created successfully at: {engine2._db_video_path}")
        print(f"Final video duration: {engine2._db_duration} seconds (matched to music)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Match music duration with background video
    print("\n=== Example 3: Match Music Duration with Background Video ===")
    engine3 = TextDisplayShortEngine(
        text="Testing with background video and music-matched duration!",
        duration=20,  # This will be overridden
        background_video_name="Minecraft jumping circuit",  # Background video from template
        background_music_name="Music dj quads",
        background_image_name="",  # Not using background image
        watermark="Video + Music Demo",
        language=Language.ENGLISH,
        match_music_duration=True,
    )
    
    try:
        print("Creating video with background video and music-matched duration...")
        for step_num, step_info in engine3.makeContent():
            print(f"Step {step_num}: {step_info}")
        print(f"✅ Video created successfully at: {engine3._db_video_path}")
        print(f"Final video duration: {engine3._db_duration} seconds (matched to music)")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 