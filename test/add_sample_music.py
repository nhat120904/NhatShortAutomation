import os
from pathlib import Path

from shortGPT.config.asset_db import AssetDatabase, AssetType


def add_sample_music():
    """
    Check for and add a sample background music asset if none exists
    """
    # Check if we already have background music assets
    all_assets = AssetDatabase.get_all_assets()
    music_assets = [
        asset
        for asset in all_assets
        if asset.get("type") == AssetType.BACKGROUND_MUSIC.value
    ]

    if not music_assets:
        print("No background music assets found. Adding a sample background music...")

        # Create public directory if it doesn't exist
        os.makedirs("public", exist_ok=True)

        # Add a sample background music
        sample_path = Path("public/sample_background_music.mp3")

        # Check if the file already exists locally
        if not sample_path.exists():
            # If not, you have a few options:
            # 1. Download a royalty-free sample from a URL
            try:
                import urllib.request

                # Replace this URL with a valid royalty-free music file
                music_url = (
                    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
                )
                print(f"Downloading sample music from {music_url}")
                urllib.request.urlretrieve(music_url, sample_path)
                print(f"Downloaded sample music to {sample_path}")
            except Exception as e:
                print(f"Failed to download sample music: {e}")
                return

        # Add to database
        if sample_path.exists():
            AssetDatabase.add_local_asset(
                name="sample_background_music",
                asset_type=AssetType.BACKGROUND_MUSIC,
                path=str(sample_path),
            )
            print("Added sample background music to asset database")
    else:
        print(f"Already have {len(music_assets)} background music assets")


if __name__ == "__main__":
    add_sample_music()
