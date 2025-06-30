import os
import time
import traceback

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       ELEVEN_SUPPORTED_LANGUAGES,
                                       LANGUAGE_ACRONYM_MAPPING,
                                       Language)
from shortGPT.engine.facts_short_engine import FactsShortEngine
from shortGPT.engine.reddit_short_engine import RedditShortEngine
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine
from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine
from shortGPT.editing_utils.video_effects import get_video_effect_options

class ShortAutomationUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI
        self.embedHTML = '<div style="display: flex; overflow-x: auto; gap: 20px;">'
        self.progress_counter = 0
        self.short_automation = None

    def create_ui(self):
        with gr.Row(visible=False) as short_automation:
            with gr.Column():
                numShorts = gr.Number(label="Number of shorts", minimum=1, value=1)
                short_type = gr.Radio(["Reddit Story shorts", "Historical Facts shorts", "Scientific Facts shorts", "Custom Facts shorts", "Custom Text shorts", "Custom Audio shorts", "Text Display shorts"], label="Type of shorts generated", value="Reddit Story shorts", interactive=True)
                facts_subject = gr.Textbox(label="Write a subject for your facts (example: Football facts)", interactive=True, visible=False)
                custom_text = gr.Textbox(label="Write your custom text content for the video", interactive=True, visible=False, lines=5, placeholder="Enter the text you want to be spoken in the video...")
                custom_audio = gr.File(label="Upload your audio file (MP3, WAV, M4A, etc.)", interactive=True, visible=False, file_types=["audio"])
                display_text = gr.Textbox(label="Text to display in the video", interactive=True, visible=False, lines=5, placeholder="Enter the text you want to display in the video...")
                video_duration = gr.Slider(minimum=1, maximum=60, value=15, step=1, label="Video duration (seconds)", visible=False)
                
                def on_short_type_change(x):
                    return (
                        gr.update(visible=x == "Custom Facts shorts"),
                        gr.update(visible=x == "Custom Text shorts"),
                        gr.update(visible=x == "Custom Audio shorts"),
                        gr.update(visible=x == "Text Display shorts"),
                        gr.update(visible=x == "Text Display shorts")
                    )
                
                short_type.change(on_short_type_change, [short_type], [facts_subject, custom_text, custom_audio, display_text, video_duration])
                tts_engine = gr.Radio([AssetComponentsUtils.ELEVEN_TTS, AssetComponentsUtils.EDGE_TTS], label="Text to speech engine", value=AssetComponentsUtils.EDGE_TTS, interactive=True)
                tts_info = gr.HTML("ℹ️ TTS settings are not used for Custom Audio shorts or Text Display shorts since you're either uploading your own audio or displaying text only", visible=False)
                self.tts_engine = tts_engine.value
                with gr.Column(visible=False) as eleven_tts:
                    language_eleven = gr.Radio([lang.value for lang in ELEVEN_SUPPORTED_LANGUAGES], label="Language", value="English", interactive=True)
                    voice_eleven = AssetComponentsUtils.voiceChoice(provider=AssetComponentsUtils.ELEVEN_TTS)
                with gr.Column(visible=True) as edge_tts:
                    language_edge = gr.Dropdown([lang.value.upper() for lang in Language], label="Language", value="ENGLISH", interactive=True)
                
                def update_tts_visibility(short_type_val):
                    is_custom_audio = short_type_val == "Custom Audio shorts"
                    is_text_display = short_type_val == "Text Display shorts"
                    return (
                        gr.update(visible=not (is_custom_audio or is_text_display)),  # tts_engine
                        gr.update(visible=(is_custom_audio or is_text_display)),      # tts_info
                        gr.update(visible=not (is_custom_audio or is_text_display) and self.tts_engine == AssetComponentsUtils.ELEVEN_TTS),  # eleven_tts
                        gr.update(visible=not (is_custom_audio or is_text_display) and self.tts_engine == AssetComponentsUtils.EDGE_TTS)     # edge_tts
                    )
                
                short_type.change(update_tts_visibility, [short_type], [tts_engine, tts_info, eleven_tts, edge_tts])
                def tts_engine_change(x):
                    self.tts_engine = x
                    return gr.update(visible=x == AssetComponentsUtils.ELEVEN_TTS), gr.update(visible=x == AssetComponentsUtils.EDGE_TTS)
                tts_engine.change(tts_engine_change, tts_engine, [eleven_tts, edge_tts])

                useImages = gr.Checkbox(label="Use images", value=True)
                numImages = gr.Radio([5, 10, 25], value=10, label="Number of images per short", visible=True, interactive=True)
                useImages.change(lambda x: gr.update(visible=x), useImages, numImages)

                addWatermark = gr.Checkbox(label="Add watermark")
                watermark = gr.Textbox(label="Watermark (your channel name)", visible=False)
                addWatermark.change(lambda x: gr.update(visible=x), [addWatermark], [watermark])

                # Background selection
                background_type = gr.Radio(["Background Video", "Background Image"], label="Background Type", value="Background Video", interactive=True)
                
                with gr.Column(visible=True) as background_video_section:
                    AssetComponentsUtils.background_video_checkbox()
                
                with gr.Column(visible=False) as background_image_section:
                    AssetComponentsUtils.background_image_checkbox()
                
                def on_background_type_change(bg_type):
                    return (
                        gr.update(visible=bg_type == "Background Video"),
                        gr.update(visible=bg_type == "Background Image")
                    )
                
                background_type.change(on_background_type_change, [background_type], [background_video_section, background_image_section])
                
                AssetComponentsUtils.background_music_checkbox()
                
                # Video Effects Section
                with gr.Column():
                    gr.HTML("<h3>🎨 Video Effects</h3>")
                    video_effect_options = get_video_effect_options()
                    video_effect_names = list(video_effect_options.keys())
                    video_effect = gr.Dropdown(
                        choices=video_effect_names,
                        value="None",
                        label="Video Effect",
                        info="Choose a visual effect to apply to your video"
                    )
                    
                    # Effect parameters (visible based on selected effect)
                    with gr.Column(visible=False) as darkness_params:
                        darkness_factor = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.6,
                            step=0.1,
                            label="Darkness Factor",
                            info="0.0 = completely black, 1.0 = original brightness"
                        )
                    
                    with gr.Column(visible=False) as vignette_params:
                        vignette_strength = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.6,
                            step=0.1,
                            label="Vignette Strength",
                            info="0.0 = no effect, 1.0 = maximum vignette"
                        )
                    
                    def on_video_effect_change(effect):
                        show_darkness = effect in ["Dark Sepia Tone", "Darken Video"]
                        show_vignette = effect == "Vignette Effect"
                        return (
                            gr.update(visible=show_darkness),
                            gr.update(visible=show_vignette)
                        )
                    
                    video_effect.change(
                        on_video_effect_change,
                        [video_effect],
                        [darkness_params, vignette_params]
                    )
                
                createButton = gr.Button("Create Shorts")

                generation_error = gr.HTML(visible=False)
                video_folder = gr.Button("📁", visible=True)
                output = gr.HTML('<div style="min-height: 80px;"></div>')

            video_folder.click(lambda _: AssetComponentsUtils.start_file(os.path.abspath("videos/")))

            createButton.click(self.inspect_create_inputs, inputs=[AssetComponentsUtils.background_video_checkbox(), AssetComponentsUtils.background_music_checkbox(), AssetComponentsUtils.background_image_checkbox(), background_type, watermark, short_type, facts_subject, custom_text, custom_audio, display_text], outputs=[generation_error]).success(self.create_short, inputs=[
                numShorts,
                short_type,
                tts_engine,
                language_eleven,
                language_edge,
                numImages,
                watermark,
                AssetComponentsUtils.background_video_checkbox(),
                AssetComponentsUtils.background_music_checkbox(),
                AssetComponentsUtils.background_image_checkbox(),
                background_type,
                facts_subject,
                voice_eleven,
                custom_text,
                custom_audio,
                display_text,
                video_duration,
                video_effect,
                darkness_factor,
                vignette_strength,
            ], outputs=[output, video_folder, generation_error])
        self.short_automation = short_automation
        return self.short_automation

    def create_short(self, numShorts, short_type, tts_engine, language_eleven, language_edge, numImages, watermark, background_video_list, background_music_list, background_image_list, background_type, facts_subject, voice_eleven, custom_text, custom_audio, display_text, video_duration, video_effect, darkness_factor, vignette_strength, progress=gr.Progress()):
        '''Creates a short'''

        try:
            numShorts = int(numShorts)
            numImages = int(numImages) if numImages else None
            
            # Prepare video effect parameters
            video_effect_params = {}
            if video_effect in ["Dark Sepia Tone", "Darken Video"]:
                video_effect_params["darkness_factor"] = darkness_factor
            elif video_effect == "Vignette Effect":
                video_effect_params["strength"] = vignette_strength
            
            # Convert effect name to enum value - handle all possible UI states
            if video_effect is None or video_effect == "None" or video_effect == "":
                video_effect_value = "none"
            else:
                video_effect_options = get_video_effect_options()
                video_effect_enum = video_effect_options.get(video_effect)
                if video_effect_enum is not None:
                    video_effect_value = video_effect_enum.value
                else:
                    video_effect_value = "none"
            
            # Choose background assets based on type
            if background_type == "Background Video":
                background_videos = (background_video_list * ((numShorts // len(background_video_list)) + 1))[:numShorts]
                background_images = [None] * numShorts
            else:  # Background Image
                background_videos = [None] * numShorts
                background_images = (background_image_list * ((numShorts // len(background_image_list)) + 1))[:numShorts]
            
            # Handle background music assignment - optional
            if background_music_list:
                background_musics = (background_music_list * ((numShorts // len(background_music_list)) + 1))[:numShorts]
            else:
                background_musics = [""] * numShorts  # Empty string for no background music
            
            # For Custom Audio shorts and Text Display shorts, we don't need TTS
            if short_type in ["Custom Audio shorts", "Text Display shorts"]:
                voice_module = None
                language = Language.ENGLISH  # Default language, not used for audio processing
            elif tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                language = Language(language_eleven.lower().capitalize())
                voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVENLABS_API_KEY'), voice_eleven, checkElevenCredits=True)
            elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                language = Language(language_edge.lower().capitalize())
                voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])
            for i in range(numShorts):
                shortEngine = self.create_short_engine(short_type=short_type, voice_module=voice_module, language=language, numImages=numImages, watermark=watermark,
                                                       background_video=background_videos[i], background_music=background_musics[i], background_image=background_images[i], facts_subject=facts_subject, custom_text=custom_text, custom_audio=custom_audio, display_text=display_text, video_duration=video_duration, video_effect=video_effect_value, video_effect_params=video_effect_params)
                num_steps = shortEngine.get_total_steps()

                def logger(prog_str):
                    progress(self.progress_counter / (num_steps * numShorts), f"Making short {i+1}/{numShorts} - {prog_str}")
                shortEngine.set_logger(logger)

                for step_num, step_info in shortEngine.makeContent():
                    print(step_num, step_info,self.progress_counter )
                    progress(self.progress_counter / (num_steps * numShorts), f"Making short {i+1}/{numShorts} - {step_info}")
                    self.progress_counter += 1

                video_path = shortEngine.get_video_output_path()
                current_url = self.shortGptUI.share_url+"/" if self.shortGptUI.share else self.shortGptUI.local_url
                file_url_path = f"{current_url}gradio_api/file={video_path}"
                file_name = video_path.split("/")[-1].split("\\")[-1]
                self.embedHTML += f'''
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <video width="{250}" height="{500}" style="max-height: 100%;" controls>
                        <source src="{file_url_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                        <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                    </a>
                </div>'''
                yield self.embedHTML + '</div>', gr.update(visible=True), gr.update(visible=False)
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
            print("Error", traceback_str)
            error_html = GradioComponentsHTML.get_html_error_template().format(error_message=error_name, stack_trace=traceback_str)
            yield self.embedHTML + '</div>', gr.update(visible=True), gr.update(value=error_html, visible=True)

    def inspect_create_inputs(self, background_video_list, background_music_list, background_image_list, background_type, watermark, short_type, facts_subject, custom_text, custom_audio, display_text, progress=gr.Progress()):
        if short_type == "Custom Facts shorts":
            if not facts_subject:
                raise gr.Error("Please write down your facts short's subject")
        if short_type == "Custom Text shorts":
            if not custom_text or not custom_text.strip():
                raise gr.Error("Please provide custom text content for the video")
        if short_type == "Custom Audio shorts":
            if not custom_audio:
                raise gr.Error("Please upload an audio file for the video")
            # Validate audio file extension
            if custom_audio and hasattr(custom_audio, 'name'):
                audio_ext = custom_audio.name.lower().split('.')[-1] if '.' in custom_audio.name else ''
                allowed_exts = ['mp3', 'wav', 'm4a', 'aac', 'flac', 'ogg']
                if audio_ext not in allowed_exts:
                    raise gr.Error(f"Unsupported audio format. Please use: {', '.join(allowed_exts)}")
        if short_type == "Text Display shorts":
            if not display_text or not display_text.strip():
                raise gr.Error("Please provide text to display in the video")
        
        # Validate background selection based on type
        if background_type == "Background Video":
            if not background_video_list:
                raise gr.Error("Please select at least one background video.")
        else:  # Background Image
            if not background_image_list:
                raise gr.Error("Please select at least one background image.")

        # Background music is now optional - no validation required

        if watermark != "":
            if not watermark.replace(" ", "").isalnum():
                raise gr.Error("Watermark should only contain letters and numbers.")
            if len(watermark) > 25:
                raise gr.Error("Watermark should not exceed 25 characters.")
            if len(watermark) < 3:
                raise gr.Error("Watermark should be at least 3 characters long.")

        # Skip LLM API key validation for Custom Text shorts, Custom Audio shorts, and Text Display shorts since we don't need LLM
        if short_type not in ["Custom Text shorts", "Custom Audio shorts", "Text Display shorts"]:
            openai_key = ApiKeyManager.get_api_key("OPENAI_API_KEY")
            gemini_key = ApiKeyManager.get_api_key("GEMINI_API_KEY")
            if not openai_key and not gemini_key:
                raise gr.Error("GEMINI OR OPENAI API key is missing. Please go to the config tab and enter the API key.")
        
        # Skip TTS API key validation for Custom Audio shorts and Text Display shorts since we don't need TTS
        if short_type not in ["Custom Audio shorts", "Text Display shorts"]:
            eleven_labs_key = ApiKeyManager.get_api_key("ELEVENLABS_API_KEY")
            if self.tts_engine == AssetComponentsUtils.ELEVEN_TTS and not eleven_labs_key:
                raise gr.Error("ELEVENLABS_API_KEY API key is missing. Please go to the config tab and enter the API key.")
        return gr.update(visible=False)

    def create_short_engine(self, short_type, voice_module, language, numImages, watermark, background_video, background_music, background_image, facts_subject, custom_text=None, custom_audio=None, display_text=None, video_duration=None, video_effect=None, video_effect_params=None):
        if short_type == "Reddit Story shorts":
            return RedditShortEngine(voice_module, background_video_name=background_video, background_music_name=background_music or "", num_images=numImages, watermark=watermark, language=language, video_effect=video_effect, video_effect_params=video_effect_params)
        if short_type == "Custom Text shorts":
            return CustomTextShortEngine(voice_module, custom_text=custom_text, background_video_name=background_video or "", background_music_name=background_music or "", background_image_name=background_image or "", num_images=numImages, watermark=watermark, language=language, video_effect=video_effect, video_effect_params=video_effect_params)
        if short_type == "Custom Audio shorts":
            # Extract the file path from the uploaded file
            custom_audio_path = custom_audio.name if custom_audio and hasattr(custom_audio, 'name') else custom_audio
            return CustomAudioShortEngine(voice_module, custom_audio_path=custom_audio_path, background_video_name=background_video or "", background_music_name=background_music or "", background_image_name=background_image or "", num_images=numImages, watermark=watermark, language=language, video_effect=video_effect, video_effect_params=video_effect_params)
        if short_type == "Text Display shorts":
            return TextDisplayShortEngine(text=display_text, duration=video_duration, background_video_name=background_video or "", background_music_name=background_music or "", background_image_name=background_image or "", watermark=watermark, language=language, video_effect=video_effect, video_effect_params=video_effect_params)
        if "fact" in short_type.lower():
            if "custom" in short_type.lower():
                facts_subject = facts_subject
            else:
                facts_subject = short_type
            return FactsShortEngine(voice_module, facts_type=facts_subject, background_video_name=background_video, background_music_name=background_music or "", num_images=numImages, watermark=watermark, language=language, video_effect=video_effect, video_effect_params=video_effect_params)
        raise gr.Error(f"Short type does not have a valid short engine: {short_type}")
