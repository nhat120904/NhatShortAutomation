# Custom Audio Upload Feature Guide

## Overview

The Custom Audio Upload feature allows users to create short videos using their own pre-recorded audio files, completely bypassing the script generation and text-to-speech (TTS) steps. This is perfect for creators who want to use professional voice recordings, podcasts clips, or any other audio content.

## 🎯 Key Benefits

- **Skip TTS Generation**: No need for TTS API keys or services
- **Professional Quality**: Use high-quality voice recordings
- **Faster Processing**: Reduces processing time by skipping 2 steps
- **Multiple Formats**: Support for MP3, WAV, M4A, AAC, FLAC, OGG
- **Seamless Integration**: Works with all existing video automation features

## 🔧 How It Works

### Traditional Workflow (Custom Text Shorts):
```
Text Input → Script Generation → TTS Generation → Audio Processing → Video + Captions → Final Video
(12 steps total)
```

### New Workflow (Custom Audio Shorts):
```
Audio Upload → Audio Processing → Video + Captions → Final Video
(10 steps total - skips steps 1 & 2)
```

## 📋 Step-by-Step Usage

### Via Web Interface:

1. **Start ShortGPT**
   ```bash
   python runShortGPT.py
   ```

2. **Navigate to Short Automation**
   - Click on the "Short Automation" tab

3. **Select Custom Audio Option**
   - Choose "Custom Audio shorts" from the dropdown

4. **Upload Your Audio**
   - Click the audio upload field
   - Select your audio file (MP3, WAV, M4A, etc.)

5. **Configure Video Settings**
   - Select background video
   - Choose background music
   - Set number of images (optional)
   - Add watermark (optional)

6. **Create Your Short**
   - Click "Create Shorts"
   - Wait for processing to complete

### Programmatic Usage:

```python
from shortGPT.engine.custom_audio_short_engine import CustomAudioShortEngine
from shortGPT.config.languages import Language

# Initialize the engine
engine = CustomAudioShortEngine(
    voiceModule=None,  # Not needed for audio upload
    custom_audio_path="/path/to/your/audio.mp3",
    background_video_name="minecraft_parkour_4k.mp4",
    background_music_name="lofi.mp3",
    language=Language.ENGLISH,
    num_images=10,
    watermark="Your Channel Name",
    short_id="my_custom_audio_short"
)

# Generate the video
for step_num, step_info in engine.makeContent():
    print(f"Step {step_num}: {step_info}")

# Get the output video path
video_path = engine.get_video_output_path()
print(f"Video created: {video_path}")
```

## 🎵 Supported Audio Formats

| Format | Extension | Auto-Conversion |
|--------|-----------|-----------------|
| WAV    | .wav      | ✅ Native       |
| MP3    | .mp3      | ✅ Via FFmpeg   |
| M4A    | .m4a      | ✅ Via FFmpeg   |
| AAC    | .aac      | ✅ Via FFmpeg   |
| FLAC   | .flac     | ✅ Via FFmpeg   |
| OGG    | .ogg      | ✅ Via FFmpeg   |

## 🎬 Video Processing Steps

When using Custom Audio Shorts, the engine performs these steps:

1. **Audio Validation**: Check if audio file exists and format is supported
2. **Audio Conversion**: Convert to WAV format if needed using FFmpeg
3. **Caption Timing**: Generate timed captions based on audio duration
4. **Background Music**: Select and prepare background music
5. **Background Video**: Select and prepare background video
6. **Asset Preparation**: Prepare custom assets (images, etc.)
7. **Video Editing**: Combine all elements into final video
8. **YouTube Metadata**: Add metadata for upload (if configured)

## ⚙️ Configuration Options

### Required Parameters:
- `custom_audio_path`: Path to your audio file
- `background_video_name`: Background video from assets
- `background_music_name`: Background music from assets

### Optional Parameters:
- `num_images`: Number of images to include (default: None)
- `watermark`: Text watermark for the video
- `language`: Language setting (affects captions)
- `short_id`: Unique identifier for the short

## 🚨 Important Notes

### Audio Quality Recommendations:
- **Sample Rate**: 44.1kHz recommended
- **Bit Depth**: 16-bit or higher
- **Duration**: Under 60 seconds for optimal shorts
- **Volume**: Consistent levels, avoid clipping
- **Clarity**: Clear speech without background noise

### TTS Settings:
- TTS engine selection is hidden for Custom Audio shorts
- Voice selection is not applicable
- Language setting is used for caption generation only

### API Requirements:
- **No TTS API keys needed** (ElevenLabs, Azure, etc.)
- OpenAI/Gemini API still required for other short types
- Background video and music assets must be configured

## 🛠️ Technical Implementation

### Engine Architecture:
```
CustomAudioShortEngine extends ContentShortEngine
├── _generateScript() → Sets placeholder script
├── _generateTempAudio() → Processes uploaded audio
├── _speedUpAudio() → Uses audio as-is (no speed changes)
└── Other steps → Standard video processing
```

### Audio Processing:
```python
# Audio conversion using FFmpeg
subprocess.run([
    'ffmpeg', '-loglevel', 'error', 
    '-i', input_audio, 
    '-ar', '44100', '-ac', '2', 
    output_wav
])
```

## 🐛 Troubleshooting

### Common Issues:

1. **"Audio file does not exist"**
   - Check file path is correct
   - Ensure file has proper permissions

2. **"Unsupported audio format"**
   - Use supported formats: MP3, WAV, M4A, AAC, FLAC, OGG
   - Check file extension matches actual format

3. **"FFmpeg conversion failed"**
   - Ensure FFmpeg is installed and in PATH
   - Check audio file isn't corrupted

4. **Video generation fails**
   - Verify background video and music are selected
   - Check asset library has required files

### Debug Mode:
Enable detailed logging by setting debug mode in the engine initialization.

## 🔄 Migration from Custom Text

If you're currently using Custom Text shorts and want to switch to Custom Audio:

1. **Record your text using TTS** or professional recording
2. **Save as supported audio format**
3. **Switch to Custom Audio shorts** in the UI
4. **Upload your audio file** instead of entering text
5. **Keep same background settings**

## 📊 Performance Comparison

| Feature | Custom Text | Custom Audio | Improvement |
|---------|-------------|--------------|-------------|
| Setup Time | Manual text entry | File upload | Faster |
| Processing Steps | 12 steps | 10 steps | 16% fewer |
| API Dependencies | TTS + LLM | None | Reduced costs |
| Audio Quality | TTS limited | Professional | Higher quality |
| Processing Time | Full pipeline | Skip 2 steps | ~20% faster |

## 🎉 Use Cases

### Perfect For:
- **Podcasters**: Convert podcast clips to short videos
- **Voice Actors**: Use professional recordings
- **Multilingual Content**: Use native speaker recordings
- **Music Content**: Add narration over music
- **Educational**: Use recorded lectures or explanations
- **Business**: Use professional announcements

### Example Workflows:
1. **Podcast Highlights**: Extract best moments → Upload audio → Generate short
2. **Product Reviews**: Record review → Upload → Create promo video
3. **Tutorials**: Record explanation → Upload → Add visual elements
4. **Announcements**: Record message → Upload → Create branded video

## 💡 Tips & Best Practices

1. **Audio Preparation**:
   - Normalize audio levels
   - Remove background noise
   - Keep consistent volume

2. **Content Strategy**:
   - Keep audio under 60 seconds
   - Include clear call-to-action
   - Match audio to visual content

3. **Technical Tips**:
   - Test with short clips first
   - Use high-quality source audio
   - Preview before final generation

## 🔗 Related Features

- **Custom Text Shorts**: For text-based content
- **Asset Library**: Manage background videos and music
- **Video Translation**: Translate existing shorts
- **Batch Processing**: Create multiple shorts at once

## 📝 Changelog

### Version 1.0 (Current)
- Initial implementation of Custom Audio Upload
- Support for 6 audio formats
- UI integration with Short Automation
- FFmpeg-based audio conversion
- Automatic TTS bypass

---

**Need help?** Check the troubleshooting section or refer to the main ShortGPT documentation.
