from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine
from shortGPT.config.languages import Language

def main():
    # Example text to display
    text = "Welcome to our channel! Don't forget to like and subscribe for more content!"
    
    # Create the engine instance
    # You can choose either background_video_name or background_image_name
    engine = TextDisplayShortEngine(
        text=text,
        duration=15,  # 15 seconds video
        background_video_name="",  # Leave empty if using background image
        background_music_name="background_music_1",  # Choose from available background music
        background_image_name="background_image_1",  # Choose from available background images
        watermark="Your Channel Name",  # Optional watermark
        language=Language.ENGLISH
    )
    
    # Run the engine to generate the video
    engine.run()
    
    # The video will be saved in the engine's dynamic asset directory
    print(f"Video generated successfully at: {engine._db_video_path}")

if __name__ == "__main__":
    main() 