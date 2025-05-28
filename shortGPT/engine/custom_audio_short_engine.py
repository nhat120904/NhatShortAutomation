from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import Language
from shortGPT.engine.content_short_engine import ContentShortEngine
from shortGPT.editing_framework.editing_engine import (EditingEngine,
                                                       EditingStep)
from shortGPT.audio.audio_duration import get_asset_duration
from shortGPT.audio import audio_utils
import os
import shutil

class CustomAudioShortEngine(ContentShortEngine):

    def __init__(self, voiceModule: VoiceModule, custom_audio_path: str, background_video_name: str, background_music_name: str, short_id="",
                 num_images=None, watermark=None, language: Language = Language.ENGLISH):
        super().__init__(short_id=short_id, short_type="custom_audio_shorts", background_video_name=background_video_name, background_music_name=background_music_name,
                 num_images=num_images, watermark=watermark, language=language, voiceModule=voiceModule)
        
        self._db_custom_audio_path = custom_audio_path
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
        Skip script generation since we're using uploaded audio directly.
        Set a placeholder script for downstream processes that might need it.
        """
        self._db_script = "Custom audio content (script generated from uploaded audio)"

    def _generateTempAudio(self):
        """
        Skip audio generation and use the uploaded audio file directly.
        Copy the uploaded audio to the temp audio path.
        """
        if not self._db_custom_audio_path:
            raise ValueError("Custom audio path cannot be empty. Please upload an audio file.")
        
        if not os.path.exists(self._db_custom_audio_path):
            raise ValueError(f"Audio file does not exist: {self._db_custom_audio_path}")
        
        # Copy the uploaded audio to our temp location
        temp_audio_path = self.dynamicAssetDir + "temp_audio_path.wav"
        
        # Convert to WAV format if needed and copy
        try:
            if self._db_custom_audio_path.lower().endswith(('.mp3', '.m4a', '.aac', '.flac', '.ogg')):
                # Convert to WAV format using FFmpeg
                import subprocess
                result = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', self._db_custom_audio_path, 
                                       '-ar', '44100', '-ac', '2', temp_audio_path], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"FFmpeg conversion failed: {result.stderr}")
            else:
                # If already WAV or supported format, just copy
                shutil.copy2(self._db_custom_audio_path, temp_audio_path)
            
            self._db_temp_audio_path = temp_audio_path
            self.logger("Using uploaded audio file as voice content")
            
        except Exception as e:
            raise ValueError(f"Failed to process uploaded audio file: {str(e)}")

    def _speedUpAudio(self):
        """
        Use the uploaded audio as-is without speed adjustment.
        Just copy temp audio to final audio path.
        """
        if self._db_audio_path:
            return
            
        self.verifyParameters(tempAudioPath=self._db_temp_audio_path)
        
        # Use the audio as-is without speed modification
        final_audio_path = self.dynamicAssetDir + "audio_voice.wav"
        shutil.copy2(self._db_temp_audio_path, final_audio_path)
        self._db_audio_path = final_audio_path
        
        self.logger("Using uploaded audio without speed modification")

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
            print("***** SCHEMA FOR RENDERING ****")
            print(videoEditor.dumpEditingSchema())
            print("***** SCHEMA FOR RENDERING ****")
            videoEditor.renderVideo(outputPath, logger= self.logger if self.logger is not self.default_logger else None)

        self._db_video_path = outputPath
