from shortGPT.config.languages import Language
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine


def main():
    # Example text to display
    text = (
        "Welcome to our channel! Don't forget to like and subscribe for more content!"
    )

    print("Demo 1: Traditional fixed duration")
    # Create the engine instance with fixed duration
    # You can choose either background_video_name or background_image_name
    engine1 = TextDisplayShortEngine(
        text=text,
        duration=15,  # 15 seconds video
        background_video_name="",  # Leave empty if using background image
        background_music_name="Music joakim karud dreams",  # Choose from available background music
        background_image_name="white_reddit_template",  # Choose from available background images
        watermark="Your Channel Name",  # Optional watermark
        language=Language.ENGLISH,
        match_music_duration=False,  # Traditional mode
    )

    # Run the engine to generate the video
    try:
        for step_num, step_info in engine1.makeContent():
            print(f"Step {step_num}: {step_info}")
        print(f"✅ Video 1 generated successfully at: {engine1._db_video_path}")
        print(f"Duration: {engine1._db_duration} seconds")
    except Exception as e:
        print(f"❌ Error creating video 1: {e}")

    print("\nDemo 2: Match music duration (NEW FEATURE!)")
    # Create the engine instance with music-matched duration
    engine2 = TextDisplayShortEngine(
        text="This video will automatically match the background music duration!",
        duration=10,  # This will be overridden by music duration
        background_video_name="",
        background_music_name="Music joakim karud dreams",  # This determines the actual duration
        background_image_name="white_reddit_template",
        watermark="Auto Duration Demo",
        language=Language.ENGLISH,
        match_music_duration=True,  # NEW FEATURE! Auto-match music duration
    )

    # Run the engine to generate the video
    try:
        for step_num, step_info in engine2.makeContent():
            print(f"Step {step_num}: {step_info}")
        print(f"✅ Video 2 generated successfully at: {engine2._db_video_path}")
        print(f"Duration: {engine2._db_duration} seconds (automatically matched to music)")
    except Exception as e:
        print(f"❌ Error creating video 2: {e}")


if __name__ == "__main__":
    main()
