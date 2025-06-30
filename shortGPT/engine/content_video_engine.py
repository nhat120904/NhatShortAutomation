import datetime
import os
import random
import re
import shutil

from shortGPT.api_utils.pexels_api import getBestVideo
from shortGPT.audio import audio_utils
from shortGPT.audio.audio_duration import get_asset_duration
from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.asset_db import AssetDatabase, AssetType
from shortGPT.config.languages import Language
from shortGPT.editing_framework.editing_engine import EditingEngine, EditingStep
from shortGPT.editing_utils import captions
from shortGPT.engine.abstract_content_engine import AbstractContentEngine
from shortGPT.gpt import gpt_editing, gpt_translate, gpt_yt


class ContentVideoEngine(AbstractContentEngine):

    def __init__(
        self,
        voiceModule: VoiceModule,
        script: str,
        background_music_name="",
        id="",
        watermark=None,
        isVerticalFormat=False,
        language: Language = Language.ENGLISH,
        auto_music=True,
        persistent_text=None,
    ):
        super().__init__(id, "general_video", language, voiceModule)
        if not id:
            if watermark:
                self._db_watermark = watermark
            self._db_auto_music = auto_music
            if background_music_name:
                self._db_background_music_name = background_music_name
            else:
                self._db_background_music_name = ""
            self._db_script = script
            self._db_format_vertical = isVerticalFormat
            self._db_persistent_text = persistent_text

        self.stepDict = {
            1: self._generateTempAudio,
            2: self._speedUpAudio,
            3: self._timeCaptions,
            4: self._generateVideoSearchTerms,
            5: self._generateVideoUrls,
            6: self._chooseBackgroundMusic,
            7: self._prepareBackgroundAssets,
            8: self._prepareCustomAssets,
            9: self._editAndRenderShort,
            10: self._addMetadata,
        }

    def _generateTempAudio(self):
        if not self._db_script:
            raise NotImplementedError("generateScript method must set self._db_script.")
        if self._db_temp_audio_path:
            return
        self.verifyParameters(text=self._db_script)
        script = self._db_script
        if self._db_language != Language.ENGLISH.value:
            self._db_translated_script = gpt_translate.translateContent(
                script, self._db_language
            )
            script = self._db_translated_script
        self._db_temp_audio_path = self.voiceModule.generate_voice(
            script, self.dynamicAssetDir + "temp_audio_path.wav"
        )

    def _speedUpAudio(self):
        if self._db_audio_path:
            return
        self.verifyParameters(tempAudioPath=self._db_temp_audio_path)
        # Since the video is not supposed to be a short( less than 60sec), there is no reason to speed it up
        self._db_audio_path = self._db_temp_audio_path
        return
        self._db_audio_path = audio_utils.speedUpAudio(
            self._db_temp_audio_path, self.dynamicAssetDir + "audio_voice.wav"
        )

    def _timeCaptions(self):
        self.verifyParameters(audioPath=self._db_audio_path)
        whisper_analysis = audio_utils.audioToText(self._db_audio_path)
        max_len = 15
        if not self._db_format_vertical:
            max_len = 30
        self._db_timed_captions = captions.getCaptionsWithTime(
            whisper_analysis, maxCaptionSize=max_len
        )

    def _generateVideoSearchTerms(self):
        self.verifyParameters(captionsTimed=self._db_timed_captions)
        # Returns a list of pairs of timing (t1,t2) + 3 search video queries, such as: [[t1,t2], [search_query_1, search_query_2, search_query_3]]
        self._db_timed_video_searches = gpt_editing.getVideoSearchQueriesTimed(
            self._db_timed_captions
        )

    def _generateVideoUrls(self):
        timed_video_searches = self._db_timed_video_searches
        self.verifyParameters(captionsTimed=timed_video_searches)
        timed_video_urls = []
        used_links = []
        for (t1, t2), search_terms in timed_video_searches:
            url = ""
            for query in reversed(search_terms):
                url = getBestVideo(
                    query,
                    orientation_landscape=not self._db_format_vertical,
                    used_vids=used_links,
                )
                if url:
                    used_links.append(url.split(".hd")[0])
                    break
            timed_video_urls.append([[t1, t2], url])
        self._db_timed_video_urls = timed_video_urls

    def _chooseBackgroundMusic(self):
        try:
            if self._db_auto_music:
                # Get all available background music assets
                all_assets = AssetDatabase.get_all_assets()

                # Important: Use AssetType.BACKGROUND_MUSIC.value to match enum value "background music"
                music_assets = [
                    asset
                    for asset in all_assets
                    if asset.get("type") == AssetType.BACKGROUND_MUSIC.value
                ]

                print(f"Found {len(music_assets)} background music assets")

                if music_assets:
                    # Randomly select a background music
                    selected_music = random.choice(music_assets)
                    self._db_background_music_name = selected_music.get("name")
                    # Get properly formatted URL using Asset Database like ContentShortEngine does
                    try:
                        self._db_background_music_url = AssetDatabase.get_asset_link(
                            self._db_background_music_name
                        )
                        print(
                            f"Selected background music: {self._db_background_music_name}"
                        )
                    except Exception as e:
                        print(f"Error getting music asset link: {e}")
                        self._db_background_music_url = None
                else:
                    print("No background music assets found in database")
                    self._db_background_music_url = None
            elif self._db_background_music_name:
                try:
                    # Use same approach as ContentShortEngine
                    self._db_background_music_url = AssetDatabase.get_asset_link(
                        self._db_background_music_name
                    )
                    print(
                        f"Using specified background music: {self._db_background_music_name}"
                    )
                except Exception as e:
                    print(f"Error getting background music asset: {e}")
                    self._db_background_music_url = None
            else:
                print("No background music specified and auto_music is disabled")
                self._db_background_music_url = None
        except Exception as e:
            print(f"Error in _chooseBackgroundMusic: {e}")
            self._db_background_music_url = None

    def _prepareBackgroundAssets(self):
        self.verifyParameters(voiceover_audio_url=self._db_audio_path)
        if not self._db_voiceover_duration:
            self.logger("Rendering short: (1/4) preparing voice asset...")
            self._db_audio_path, self._db_voiceover_duration = get_asset_duration(
                self._db_audio_path, isVideo=False
            )

    def _prepareCustomAssets(self):
        self.logger("Rendering short: (3/4) preparing custom assets...")
        pass

    def _editAndRenderShort(self):
        self.verifyParameters(voiceover_audio_url=self._db_audio_path)

        outputPath = self.dynamicAssetDir + "rendered_video.mp4"
        if not (os.path.exists(outputPath)):
            self.logger("Rendering short: Starting automated editing...")
            videoEditor = EditingEngine()
            videoEditor.addEditingStep(
                EditingStep.ADD_VOICEOVER_AUDIO, {"url": self._db_audio_path}
            )

            # Add background music if available
            if (
                hasattr(self, "_db_background_music_url")
                and self._db_background_music_url
            ):
                try:
                    print(f"Adding background music: {self._db_background_music_url}")
                    videoEditor.addEditingStep(
                        EditingStep.ADD_BACKGROUND_MUSIC,
                        {
                            "url": self._db_background_music_url,
                            "loop_background_music": self._db_voiceover_duration,
                            "volume_percentage": 0.08,
                        },
                    )
                except Exception as e:
                    print(f"Error adding background music to video: {e}")

            for (t1, t2), video_url in self._db_timed_video_urls:
                videoEditor.addEditingStep(
                    EditingStep.ADD_BACKGROUND_VIDEO,
                    {"url": video_url, "set_time_start": t1, "set_time_end": t2},
                )

            # Add persistent text if specified
            if hasattr(self, "_db_persistent_text") and self._db_persistent_text:
                caption_type = (
                    EditingStep.ADD_CAPTION_SHORT_ARABIC
                    if self._db_language == Language.ARABIC.value
                    else EditingStep.ADD_CAPTION_SHORT
                )
                videoEditor.addEditingStep(
                    caption_type,
                    {
                        "text": self._db_persistent_text.upper(),
                        "set_time_start": 0,
                        "set_time_end": self._db_voiceover_duration,
                    },
                )

            if self._db_format_vertical:
                caption_type = (
                    EditingStep.ADD_CAPTION_SHORT_ARABIC
                    if self._db_language == Language.ARABIC.value
                    else EditingStep.ADD_CAPTION_SHORT
                )
            else:
                caption_type = (
                    EditingStep.ADD_CAPTION_LANDSCAPE_ARABIC
                    if self._db_language == Language.ARABIC.value
                    else EditingStep.ADD_CAPTION_LANDSCAPE
                )

            for (t1, t2), text in self._db_timed_captions:
                videoEditor.addEditingStep(
                    caption_type,
                    {"text": text.upper(), "set_time_start": t1, "set_time_end": t2},
                )

            videoEditor.renderVideo(
                outputPath,
                logger=self.logger if self.logger is not self.default_logger else None,
            )

        self._db_video_path = outputPath

    def _addMetadata(self):
        if not os.path.exists("videos/"):
            os.makedirs("videos")
        self._db_yt_title, self._db_yt_description = (
            gpt_yt.generate_title_description_dict(self._db_script)
        )

        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        newFileName = f"videos/{date_str} - " + re.sub(
            r"[^a-zA-Z0-9 '\n\.]", "", self._db_yt_title
        )

        # Use absolute path to prevent issues with directory changes
        abs_video_filename = os.path.abspath(newFileName + ".mp4")
        abs_txt_filename = os.path.abspath(newFileName + ".txt")
        shutil.move(self._db_video_path, abs_video_filename)
        with open(abs_txt_filename, "w", encoding="utf-8") as f:
            f.write(
                f"---Youtube title---\n{self._db_yt_title}\n---Youtube description---\n{self._db_yt_description}"
            )
        self._db_video_path = abs_video_filename
        self._db_ready_to_upload = True
