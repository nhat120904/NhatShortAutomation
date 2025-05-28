from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import Language
from shortGPT.engine.content_short_engine import ContentShortEngine
from shortGPT.editing_framework.editing_engine import (EditingEngine,
                                                       EditingStep)
import os

class CustomTextShortEngine(ContentShortEngine):

    def __init__(self, voiceModule: VoiceModule, custom_text: str, background_video_name: str, background_music_name: str, short_id="",
                 num_images=None, watermark=None, language: Language = Language.ENGLISH):
        super().__init__(short_id=short_id, short_type="custom_text_shorts", background_video_name=background_video_name, background_music_name=background_music_name,
                 num_images=num_images, watermark=watermark, language=language, voiceModule=voiceModule)
        
        self._db_custom_text = custom_text
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
        }

    def _generateScript(self):
        """
        Uses the provided custom text as the script instead of generating it with LLM.
        """
        if not self._db_custom_text or not self._db_custom_text.strip():
            raise ValueError("Custom text cannot be empty. Please provide text content for the video.")
        
        self._db_script = self._db_custom_text.strip() 

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
        self.verifyParameters(
            voiceover_audio_url=self._db_audio_path,
            video_duration=self._db_background_video_duration,
            music_url=self._db_background_music_url)

        outputPath = self.dynamicAssetDir+"rendered_video.mp4"
        if not (os.path.exists(outputPath)):
            self.logger("Rendering short: Starting automated editing...")
            videoEditor = EditingEngine()
            videoEditor.addEditingStep(EditingStep.ADD_VOICEOVER_AUDIO, {
                                       'url': self._db_audio_path})
            videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_MUSIC, {'url': self._db_background_music_url,
                                                                          'loop_background_music': self._db_voiceover_duration,
                                                                          "volume_percentage": 0.11})
            videoEditor.addEditingStep(EditingStep.CROP_1920x1080, {
                                       'url': self._db_background_trimmed})
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