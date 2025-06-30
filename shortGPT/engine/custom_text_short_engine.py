from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import Language
from shortGPT.engine.content_short_engine import ContentShortEngine
from shortGPT.editing_framework.editing_engine import (EditingEngine,
                                                       EditingStep)
import os

class CustomTextShortEngine(ContentShortEngine):

    def __init__(self, voiceModule: VoiceModule, custom_text: str, background_video_name: str = "", background_music_name: str = "", background_image_name: str = "", short_id="",
                 num_images=None, watermark=None, language: Language = Language.ENGLISH, video_effect=None, video_effect_params=None):
        # Initialize with background_video_name even if using image (for compatibility)
        super().__init__(short_id=short_id, short_type="custom_text_shorts", background_video_name=background_video_name, background_music_name=background_music_name,
                 num_images=num_images, watermark=watermark, language=language, voiceModule=voiceModule, video_effect=video_effect, video_effect_params=video_effect_params)
        
        self._db_custom_text = custom_text
        self._db_background_image_name = background_image_name
        self._use_background_image = bool(background_image_name)
        
        # Modify step dict to handle background image vs video
        if self._use_background_image:
            self.stepDict = {
                1:  self._generateScript,
                2:  self._generateTempAudio,
                3:  self._speedUpAudio,
                4:  self._timeCaptions,
                5:  self._chooseBackgroundMusic,
                6:  self._chooseBackgroundImage,
                7:  self._prepareBackgroundAssets,
                8: self._prepareCustomAssets,
                9: self._editAndRenderShort,
                10: self._addYoutubeMetadata,
            }
        else:
            self.stepDict = {
                1:  self._generateScript,
                2:  self._generateTempAudio,
                3:  self._speedUpAudio,
                4:  self._timeCaptions,
                5:  self._chooseBackgroundMusic,
                6:  self._chooseBackgroundVideo,
                7:  self._prepareBackgroundAssets,
                8: self._prepareCustomAssets,
                9: self._editAndRenderShort,
                10: self._addYoutubeMetadata,
            }

    def _generateScript(self):
        """
        Uses the provided custom text as the script instead of generating it with LLM.
        """
        if not self._db_custom_text or not self._db_custom_text.strip():
            raise ValueError("Custom text cannot be empty. Please provide text content for the video.")
        
        self._db_script = self._db_custom_text.strip() 

    def _chooseBackgroundImage(self):
        """
        Choose background image instead of background video.
        """
        from shortGPT.config.asset_db import AssetDatabase
        self._db_background_image_url = AssetDatabase.get_asset_link(
            self._db_background_image_name)

    def _prepareBackgroundAssets(self):
        """
        Prepare background assets - either video or image based on configuration.
        """
        self.verifyParameters(voiceover_audio_url=self._db_audio_path)
        if not self._db_voiceover_duration:
            self.logger("Rendering short: (1/4) preparing voice asset...")
            from shortGPT.audio.audio_duration import get_asset_duration
            self._db_audio_path, self._db_voiceover_duration = get_asset_duration(
                self._db_audio_path, isVideo=False)
        
        if self._use_background_image:
            # For background images, we don't need to trim like videos
            self.logger("Rendering short: (2/4) preparing background image asset...")
            # Image will be displayed for the entire duration of the voiceover
        else:
            # Original video preparation logic
            if not self._db_background_trimmed:
                self.logger("Rendering short: (2/4) preparing background video asset...")
                from shortGPT.editing_utils.handle_videos import extract_random_clip_from_video
                self._db_background_trimmed = extract_random_clip_from_video(
                    self._db_background_video_url, self._db_background_video_duration, self._db_voiceover_duration, self.dynamicAssetDir + "clipped_background.mp4")

    def _generateTempAudio(self):
        if not self._db_script:
            raise NotImplementedError("generateScript method must set self._db_script.")
        if (self._db_temp_audio_path):
            return
        self.verifyParameters(text=self._db_script)
        script = self._db_script
        # if (self._db_language != Language.ENGLISH.value):
        #     self._db_translated_script = gpt_translate.translateContent(script, self._db_language)
        #     script = self._db_translated_script
        self._db_temp_audio_path = self.voiceModule.generate_voice(
            script, self.dynamicAssetDir + "temp_audio_path.wav")
        
    def _editAndRenderShort(self):
        if self._use_background_image:
            # Verify parameters for background image
            self.verifyParameters(
                voiceover_audio_url=self._db_audio_path,
                background_image_url=self._db_background_image_url)
        else:
            # Original verification for background video
            self.verifyParameters(
                voiceover_audio_url=self._db_audio_path,
                video_duration=self._db_background_video_duration)

        outputPath = self.dynamicAssetDir+"rendered_video.mp4"
        if not (os.path.exists(outputPath)):
            self.logger("Rendering short: Starting automated editing...")
            videoEditor = EditingEngine()
            videoEditor.addEditingStep(EditingStep.ADD_VOICEOVER_AUDIO, {
                                       'url': self._db_audio_path})
            
            # Add background music only if it's specified
            if self._db_background_music_url:
                videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_MUSIC, {'url': self._db_background_music_url,
                                                                              'loop_background_music': self._db_voiceover_duration,
                                                                              "volume_percentage": 0.11})
            
            if self._use_background_image:
                # Add background image for the entire duration
                videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_IMAGE, {
                                           'url': self._db_background_image_url,
                                           'set_time_start': 0,
                                           'set_time_end': self._db_voiceover_duration})
            else:
                # Original background video logic
                videoEditor.addEditingStep(EditingStep.CROP_1920x1080, {
                                           'url': self._db_background_trimmed})
            
            # Apply video effect if specified
            if self._db_video_effect and self._db_video_effect != "none":
                # Ensure effect_type is never Python None
                effect_type = self._db_video_effect if self._db_video_effect is not None else "none"
                if self._use_background_image:
                    # For background images, apply effect to the generated video
                    videoEditor.addEditingStep(EditingStep.APPLY_VIDEO_EFFECT, {
                                               'url': self._db_background_image_url,
                                               'effect_type': effect_type,
                                               'effect_params': self._db_video_effect_params})
                else:
                    # For background videos, apply effect to the trimmed video
                    videoEditor.addEditingStep(EditingStep.APPLY_VIDEO_EFFECT, {
                                               'url': self._db_background_trimmed,
                                               'effect_type': effect_type,
                                               'effect_params': self._db_video_effect_params})
            
            # videoEditor.addEditingStep(EditingStep.ADD_SUBSCRIBE_ANIMATION, {'url': AssetDatabase.get_asset_link('subscribe animation')})

            if self._db_watermark:
                videoEditor.addEditingStep(EditingStep.ADD_WATERMARK, {
                                           'text': self._db_watermark})

            caption_type = EditingStep.ADD_CAPTION_SHORT_ARABIC if self._db_language == Language.ARABIC.value else EditingStep.ADD_CAPTION_SHORT
            for timing, text in self._db_timed_captions:
                videoEditor.addEditingStep(caption_type, {'text': text.upper(),
                                                          'set_time_start': timing[0],
                                                          'set_time_end': timing[1]})
            # if self._db_num_images:
            #     for timing, image_url in self._db_timed_image_urls:
            #         videoEditor.addEditingStep(EditingStep.SHOW_IMAGE, {'url': image_url,
            #                                                             'set_time_start': timing[0],
            #                                                             'set_time_end': timing[1]})
            print("***** SCHEMA FOR RENDERING ****")
            print(videoEditor.dumpEditingSchema())
            print("***** SCHEMA FOR RENDERING ****")
            videoEditor.renderVideo(outputPath, logger= self.logger if self.logger is not self.default_logger else None)

        self._db_video_path = outputPath