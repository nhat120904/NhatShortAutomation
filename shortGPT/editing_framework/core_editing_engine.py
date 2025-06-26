from urllib.error import HTTPError
from shortGPT.config.path_utils import get_program_path
import os
from shortGPT.config.path_utils import handle_path
import numpy as np
from typing import Any, Dict, List, Union
from moviepy import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                    TextClip, VideoFileClip, AudioClip)
from moviepy.Clip import Clip
from moviepy import vfx, afx
from shortGPT.editing_framework.rendering_logger import MoviepyProgressLogger
import json
import tempfile
import hashlib
import os

def load_schema(json_path):
    return json.loads(open(json_path, 'r', encoding='utf-8').read())

class CoreEditingEngine:

    def generate_image(self, schema:Dict[str, Any],output_file , logger=None):
        assets = dict(sorted(schema['visual_assets'].items(), key=lambda item: item[1]['z']))
        clips = []

        for asset_key in assets:
            asset = assets[asset_key]
            asset_type = asset['type']
            if asset_type == 'image':
                clip = self.process_image_asset(asset)
            elif asset_type == 'text':
                clip = self.process_text_asset(asset)
                clips.append(clip)
            else:
                raise ValueError(f'Invalid asset type: {asset_type}')
            clips.append(clip)

        image = CompositeVideoClip(clips)
        image.save_frame(output_file)
        return output_file

    def generate_video(self, schema:Dict[str, Any], output_file, logger=None, force_duration=None, threads=None) -> None:
        visual_assets = dict(sorted(schema['visual_assets'].items(), key=lambda item: item[1]['z']))
        audio_assets = dict(sorted(schema['audio_assets'].items(), key=lambda item: item[1]['z']))
        
        visual_clips = []
        for asset_key in visual_assets:
            asset = visual_assets[asset_key]
            asset_type = asset['type']
            if asset_type == 'video':
                clip = self.process_video_asset(asset)
            elif asset_type == 'image':
                # clip = self.process_image_asset(asset)
                try:
                    clip = self.process_image_asset(asset)
                except Exception as e:
                    print(f"Failed to load image {asset['parameters']['url']}. Error : {str(e)}")
                    continue
            elif asset_type == 'text':
                clip = self.process_text_asset(asset)
            else:
                raise ValueError(f'Invalid asset type: {asset_type}')

            visual_clips.append(clip)
        
        audio_clips = []

        for asset_key in audio_assets:
            asset = audio_assets[asset_key]
            asset_type = asset['type']
            if asset_type == "audio":
                audio_clip = self.process_audio_asset(asset)
            else:
                raise ValueError(f"Invalid asset type: {asset_type}")

            audio_clips.append(audio_clip)
        video = CompositeVideoClip(visual_clips)
        if(audio_clips):
            audio = CompositeAudioClip(audio_clips)
            video = video.with_audio(audio)
            video = video.with_duration(audio.duration)
        if force_duration:
            video = video.with_duration(force_duration)
        if logger:
            my_logger = MoviepyProgressLogger(callBackFunction=logger)
            video.write_videofile(output_file, threads=threads,codec='libx264', audio_codec='aac', fps=25, preset='veryfast', logger=my_logger)
        else:
            video.write_videofile(output_file, threads=threads,codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
        return output_file
    
    def generate_audio(self, schema:Dict[str, Any], output_file, logger=None) -> None:
        audio_assets = dict(sorted(schema['audio_assets'].items(), key=lambda item: item[1]['z']))
        audio_clips = []

        for asset_key in audio_assets:
            asset = audio_assets[asset_key]
            asset_type = asset['type']
            if asset_type == "audio":
                audio_clip = self.process_audio_asset(asset)
            else:
                raise ValueError(f"Invalid asset type: {asset_type}")

            audio_clips.append(audio_clip)
        audio = CompositeAudioClip(audio_clips)
        audio.fps = 44100
        if logger:
            my_logger = MoviepyProgressLogger(callBackFunction=logger)
            audio.write_audiofile(output_file, logger=my_logger)
        else:
            audio.write_audiofile(output_file)
        return output_file
    # Process common actions
    def process_common_actions(self,
                                   clip: Union[VideoFileClip, ImageClip, TextClip, AudioFileClip],
                                   actions: List[Dict[str, Any]]) -> Union[VideoFileClip, AudioFileClip, ImageClip, TextClip]:
        for action in actions:
            if action['type'] == 'set_time_start':
                clip = clip.with_start(action['param'])
                continue
   
            if action['type'] == 'set_time_end':
                clip = clip.with_end(action['param'])
                continue
            
            if action['type'] == 'subclip':
                clip = clip.subclipped(**action['param'])
                continue

        return clip

    # Process common visual clip actions
    def process_common_visual_actions(self,
                                   clip: Clip,
                                   actions: List[Dict[str, Any]]) -> Union[VideoFileClip, ImageClip, TextClip]:
        clip = self.process_common_actions(clip, actions)
        for action in actions:
 
            if action['type'] == 'resize':
                clip = clip.with_effects([vfx.Resize(**action['param'])])
                continue

            if action['type'] == 'crop':
                clip = clip.with_effects([vfx.Crop(**action['param'])])
                continue

            if action['type'] == 'screen_position':
                clip = clip.with_position(**action['param'])
                continue

            if action['type'] == 'green_screen':
                params = action['param']
                color = params['color'] if  params['color'] else [52, 255, 20]
                thr = params["threshold"] if params["threshold"] else 100
                s = params['stiffness'] if params['stiffness'] else 5
                clip = clip.with_effects([vfx.MaskColor(color=color,threshold=thr, stiffness=s)])
                continue

            if action['type'] == 'normalize_image':
                clip = clip.image_transform(self.__normalize_frame)
                continue

            if action['type'] == 'auto_resize_image':
                ar = clip.aspect_ratio
                height = action['param']['maxHeight']
                width = action['param']['maxWidth']
                if ar <1:
                    clip = clip.with_effects([vfx.Resize((height*ar, height))])
                else:
                    clip = clip.with_effects([vfx.Resize((width, width/ar))])
                continue

            if action['type'] == 'video_effect':
                from shortGPT.editing_utils.video_effects import VideoEffect, apply_video_effect
                effect_type = action['param'].get('effect_type', 'none')
                effect_params = action['param'].get('effect_params', {})
                
                try:
                    effect_enum = VideoEffect(effect_type)
                    clip = apply_video_effect(clip, effect_enum, **effect_params)
                except ValueError:
                    print(f"Warning: Unknown video effect '{effect_type}', skipping...")
                continue

        return clip

    # Process audio actions
    def process_audio_actions(self, clip: AudioClip,
                            actions: List[Dict[str, Any]]) -> AudioClip:
        clip = self.process_common_actions(clip, actions)
        for action in actions:
            if action['type'] == 'normalize_music':
                clip = clip.with_effects([afx.AudioNormalize()])
                continue

            if action['type'] == 'loop_background_music':
                target_duration = action['param']
                start = clip.duration * 0.15
                clip = clip.subclipped(start)
                clip = clip.with_effects([afx.AudioLoop(duration=target_duration)])
                continue

            if action['type'] == 'volume_percentage':
                clip = clip.with_effects([afx.MultiplyVolume(action['param'])])
                continue

        return clip
    # Process individual asset types
    def process_video_asset(self, asset: Dict[str, Any]) -> VideoFileClip:
        params = {
            'filename': handle_path(asset['parameters']['url'])
        }
        if 'audio' in asset['parameters']:
            params['audio'] = asset['parameters']['audio']
        
        # Convert m3u8 files to mp4 before processing with MoviePy
        if params['filename'].endswith('.m3u8'):
            print(f"Detected M3U8 file: {params['filename']}")
            params['filename'] = self._convert_m3u8_to_mp4(params['filename'])
            print(f"Converted to MP4: {params['filename']}")
        
        print(f"Loading video from {params['filename']}")
        if params['filename'].startswith(('http://', 'https://')):
            import urllib.request
            
            # Create a temp directory if it doesn't exist
            temp_dir = "temp_videos"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extract filename from URL
            url = params['filename']
            # Generate a hash of the URL for uniqueness
            url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
            
            # Get a safe filename - either the original if short enough or based on hash
            original_filename = url.split('/')[-1].split('?')[0]  # Remove query parameters
            if len(original_filename) > 50:  # Limit filename length
                file_ext = os.path.splitext(original_filename)[1] or '.mp4'  # Default to .mp4 if no extension
                video_filename = f"{url_hash}{file_ext}"
            else:
                video_filename = original_filename
            
            # Generate an absolute local path for the downloaded file
            local_path = os.path.abspath(os.path.join(temp_dir, video_filename))
            
            # Download the file if it doesn't exist
            if not os.path.exists(local_path):
                try:
                    print(f"Downloading video from {url} to {local_path}")
                    # Add a User-Agent header
                    req = urllib.request.Request(
                        url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    )
                    with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                        out_file.write(response.read())
                except urllib.error.HTTPError as e:
                    print(f"Failed to download video: {e}")
            
            # Update params to use the local file
            params['filename'] = local_path
        clip = VideoFileClip(**params)
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_image_asset(self, asset: Dict[str, Any]) -> ImageClip:
        url = asset['parameters']['url']
        if url.startswith(('http://', 'https://')):
            import urllib.request
            
            # Create a temp directory if it doesn't exist
            temp_dir = "temp_images"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extract filename from URL
            image_filename = url.split('/')[-1]
            # Generate a hash of the URL for uniqueness
            url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
            
            # Get a safe filename - either the original if short enough or based on hash
            original_filename = url.split('/')[-1].split('?')[0]  # Remove query parameters
            if len(original_filename) > 50:  # Limit filename length
                file_ext = os.path.splitext(image_filename)[1] or '.jpg'  # Default to .jpg if no extension
                image_filename = f"{url_hash}{file_ext}"
            else:
                image_filename = original_filename
            
            # Generate an absolute local path for the downloaded file
            local_path = os.path.abspath(os.path.join(temp_dir, image_filename))
            
            # Download the file if it doesn't exist
            if not os.path.exists(local_path):
                try:
                    print(f"Downloading image from {url} to {local_path}")
                    req = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    )
                    with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                        out_file.write(response.read())
                except urllib.error.HTTPError as e:
                    print(f"Failed to download image: {e}")
                    raise e
            
            # Update url to use the local file
            url = local_path
        
        clip = ImageClip(url)
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_text_asset(self, asset: Dict[str, Any]) -> TextClip:
        text_clip_params = asset['parameters']
        
        if not (any(key in text_clip_params for key in ['text','fontsize', 'size'])):
            raise Exception('You must include at least a size or a fontsize to determine the size of your text')
        text_method = text_clip_params.get('method', 'label')
        clip_info = {
            'text': text_clip_params['text'],
            'font': text_clip_params.get('font'),
            'font_size': text_clip_params.get('font_size'),
            'color': text_clip_params.get('color'),
            'stroke_width': text_clip_params.get('stroke_width'),
            'stroke_color': text_clip_params.get('stroke_color'),
            'size': text_clip_params.get('size'),
            'method': text_method,
            'text_align': text_clip_params.get('text_align', 'center')
        }
        clip_info = {k: v for k, v in clip_info.items() if v is not None}
        clip = TextClip(**clip_info)
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_audio_asset(self, asset: Dict[str, Any]) -> AudioFileClip:
        clip = AudioFileClip(asset['parameters']['url'])
        return self.process_audio_actions(clip, asset['actions'])
    
    def __normalize_image(self, clip):
        def f(get_frame, t):
            if f.normalized_frame is not None:
                return f.normalized_frame
            else:
                frame = get_frame(t)
                f.normalized_frame = self.__normalize_frame(frame)
                return f.normalized_frame

        f.normalized_frame = None

        return clip.fl(f)


    def __normalize_frame(self, frame):
        shape = np.shape(frame)
        [dimensions, ] = np.shape(shape)

        if dimensions == 2:
            (height, width) = shape
            normalized_frame = np.zeros((height, width, 3))
            for y in range(height):
                for x in range(width):
                    grey_value = frame[y][x]
                    normalized_frame[y][x] = (grey_value, grey_value, grey_value)
            return normalized_frame
        else:
            return frame

    def _convert_m3u8_to_mp4(self, m3u8_path):
        """Convert m3u8 file to mp4 using ffmpeg"""
        import subprocess
        import os
        import hashlib
        
        # Generate output filename based on input path
        if m3u8_path.startswith(('http://', 'https://')):
            # For URLs, create a hash-based filename
            url_hash = hashlib.md5(m3u8_path.encode()).hexdigest()[:10]
            output_filename = f"converted_{url_hash}.mp4"
        else:
            # For local files, replace .m3u8 with .mp4
            output_filename = m3u8_path.replace('.m3u8', '_converted.mp4')
        
        # Ensure we have absolute path for output
        if not os.path.isabs(output_filename):
            temp_dir = "temp_videos"
            os.makedirs(temp_dir, exist_ok=True)
            output_path = os.path.abspath(os.path.join(temp_dir, output_filename))
        else:
            output_path = output_filename
        
        # Check if converted file already exists
        if os.path.exists(output_path):
            print(f"Converted file already exists: {output_path}")
            return output_path
        
        print(f"Converting M3U8 to MP4: {m3u8_path} -> {output_path}")
        
        # Use ffmpeg to convert m3u8 to mp4
        cmd = [
            'ffmpeg',
            '-i', m3u8_path,
            '-c', 'copy',  # Copy streams without re-encoding for speed
            '-avoid_negative_ts', 'make_zero',  # Handle timestamp issues
            '-y',  # Overwrite output file if it exists
            output_path
        ]
        
        try:
            # Run ffmpeg conversion
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=300  # 5 minute timeout
            )
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"Successfully converted M3U8 to MP4: {output_path}")
                return output_path
            else:
                raise Exception("Conversion completed but output file is missing or empty")
                
        except subprocess.TimeoutExpired:
            raise Exception(f"M3U8 conversion timed out after 5 minutes")
        except subprocess.CalledProcessError as e:
            error_msg = f"FFmpeg conversion failed: {e.stderr}"
            print(f"FFmpeg error: {e.stderr}")
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"M3U8 conversion failed: {str(e)}")

