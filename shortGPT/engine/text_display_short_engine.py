import os

from shortGPT.config.languages import Language
from shortGPT.editing_framework.editing_engine import EditingEngine, EditingStep
from shortGPT.engine.content_short_engine import ContentShortEngine


class TextDisplayShortEngine(ContentShortEngine):
    def __init__(
        self,
        text: str,
        duration: int,
        background_video_name: str = "",
        background_music_name: str = "",
        background_image_name: str = "",
        short_id="",
        watermark=None,
        language: Language = Language.ENGLISH,
        voiceModule=None,
        video_effect=None,
        video_effect_params=None,
    ):
        # Initialize with background_video_name even if using image (for compatibility)
        super().__init__(
            short_id=short_id,
            short_type="text_display_shorts",
            background_video_name=background_video_name,
            background_music_name=background_music_name,
            watermark=watermark,
            language=language,
            voiceModule=voiceModule,
            video_effect=video_effect,
            video_effect_params=video_effect_params,
        )

        if not 1 <= duration <= 60:
            raise ValueError("Duration must be between 1 and 60 seconds")

        self._db_custom_text = text
        self._db_background_image_name = background_image_name
        self._use_background_image = bool(background_image_name)
        self._db_duration = duration

        # Define steps for the engine
        if self._use_background_image:
            self.stepDict = {
                1: self._generateScript,
                2: self._chooseBackgroundMusic,
                3: self._chooseBackgroundImage,
                4: self._prepareBackgroundAssets,
                5: self._editAndRenderShort,
                6: self._addYoutubeMetadata,
            }
        else:
            self.stepDict = {
                1: self._generateScript,
                2: self._chooseBackgroundMusic,
                3: self._chooseBackgroundVideo,
                4: self._prepareBackgroundAssets,
                5: self._editAndRenderShort,
                6: self._addYoutubeMetadata,
            }

    def _generateScript(self):
        """Implementation of the abstract method from ContentShortEngine"""
        if not self._db_custom_text or not self._db_custom_text.strip():
            raise ValueError(
                "Text cannot be empty. Please provide text content for the video."
            )
        self._db_script = self._db_custom_text.strip()

    def _chooseBackgroundImage(self):
        """Choose background image"""
        from shortGPT.config.asset_db import AssetDatabase

        self._db_background_image_url = AssetDatabase.get_asset_link(
            self._db_background_image_name
        )

    def _prepareBackgroundAssets(self):
        """Prepare background assets - either video or image based on configuration"""
        if self._use_background_image:
            self.logger("Rendering short: (1/2) preparing background image asset...")
        else:
            if not self._db_background_trimmed:
                self.logger(
                    "Rendering short: (1/2) preparing background video asset..."
                )
                from shortGPT.editing_utils.handle_videos import (
                    extract_random_clip_from_video,
                )

                self._db_background_trimmed = extract_random_clip_from_video(
                    self._db_background_video_url,
                    self._db_background_video_duration,
                    self._db_duration,
                    self.dynamicAssetDir + "clipped_background.mp4",
                )

    def _editAndRenderShort(self):
        """Edit and render the final video"""
        if self._use_background_image:
            self.verifyParameters(background_image_url=self._db_background_image_url)
        else:
            self.verifyParameters(video_duration=self._db_background_video_duration)

        outputPath = self.dynamicAssetDir + "rendered_video.mp4"
        if not os.path.exists(outputPath):
            self.logger("Rendering short: Starting automated editing...")
            videoEditor = EditingEngine()

            # Add background music only if it's specified
            if self._db_background_music_url:
                videoEditor.addEditingStep(
                    EditingStep.ADD_BACKGROUND_MUSIC,
                    {
                        "url": self._db_background_music_url,
                        "loop_background_music": self._db_duration,
                        "volume_percentage": 0.5,
                    },
                )

            if self._use_background_image:
                # Add background image for the entire duration
                videoEditor.addEditingStep(
                    EditingStep.ADD_BACKGROUND_IMAGE,
                    {
                        "url": self._db_background_image_url,
                        "set_time_start": 0,
                        "set_time_end": self._db_duration,
                    },
                )
            else:
                # Add background video
                videoEditor.addEditingStep(
                    EditingStep.ADD_BACKGROUND_VIDEO,
                    {
                        "url": self._db_background_trimmed,
                        "set_time_start": 0,
                        "set_time_end": self._db_duration,
                    },
                )

            # Apply video effect if specified
            print(
                f"DEBUG TextDisplay: self._db_video_effect = '{self._db_video_effect}' (type: {type(self._db_video_effect)})"
            )
            if self._db_video_effect and self._db_video_effect != "none":
                print(
                    f"DEBUG TextDisplay: Adding video effect action with effect_type = '{self._db_video_effect}'"
                )
                if self._use_background_image:
                    # For background images, apply effect to the generated video
                    videoEditor.addEditingStep(
                        EditingStep.APPLY_VIDEO_EFFECT,
                        {
                            "url": self._db_background_image_url,
                            "effect_type": self._db_video_effect,
                            "effect_params": self._db_video_effect_params,
                        },
                    )
                else:
                    # For background videos, apply effect to the trimmed video
                    videoEditor.addEditingStep(
                        EditingStep.APPLY_VIDEO_EFFECT,
                        {
                            "url": self._db_background_trimmed,
                            "effect_type": self._db_video_effect,
                            "effect_params": self._db_video_effect_params,
                        },
                    )
            else:
                print(f"DEBUG TextDisplay: Skipping video effect (none or empty)")

            # Add watermark if specified
            if self._db_watermark:
                videoEditor.addEditingStep(
                    EditingStep.ADD_WATERMARK, {"text": self._db_watermark}
                )

            # Add text caption for the entire duration
            caption_type = (
                EditingStep.ADD_CAPTION_SHORT_ARABIC
                if self._db_language == Language.ARABIC.value
                else EditingStep.ADD_CAPTION_SHORT
            )
            videoEditor.addEditingStep(
                caption_type,
                {
                    "text": self._db_script.upper(),
                    "set_time_start": 0,
                    "set_time_end": self._db_duration,
                },
            )

            print("***** SCHEMA FOR RENDERING ****")
            print(videoEditor.dumpEditingSchema())
            print("***** SCHEMA FOR RENDERING ****")

            videoEditor.renderVideo(
                outputPath,
                logger=self.logger if self.logger is not self.default_logger else None,
            )

        self._db_video_path = outputPath
