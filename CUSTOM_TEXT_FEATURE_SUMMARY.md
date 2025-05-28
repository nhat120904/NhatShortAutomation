# Custom Text Feature for ShortGPT

## Overview
This feature allows users to input their own custom text instead of relying on LLM-generated content for creating short videos. The text will be converted to speech and displayed throughout the entire video with matching visuals.

## What Was Added

### 1. New Engine: `CustomTextShortEngine`
- **Location**: `shortGPT/engine/custom_text_short_engine.py`
- **Purpose**: Handles video creation using user-provided text instead of LLM generation
- **Key Features**:
  - Accepts custom text input
  - Validates that text is not empty
  - Uses the same video generation pipeline as other engines
  - Supports all existing features (images, watermarks, background music/video, etc.)

### 2. Updated User Interface
- **Location**: `gui/ui_tab_short_automation.py`
- **Changes**:
  - Added "Custom Text shorts" option to the short type dropdown
  - Added a text area for custom text input (5 lines, with placeholder)
  - Added validation for custom text content
  - Skip LLM API key validation for custom text shorts (since no LLM is needed)
  - Updated all method signatures to handle custom text parameter

### 3. Updated Imports
- **Location**: `shortGPT/engine/__init__.py`
- Added import for the new custom text engine

## How to Use

### Via GUI:
1. Run the ShortGPT application: `python runShortGPT.py`
2. Navigate to the "Shorts Automation" tab
3. Select "Custom Text shorts" from the dropdown
4. Enter your custom text in the text area that appears
5. Configure other settings (voice, background assets, etc.)
6. Click "Create Shorts" to generate your video

### Via Code:
```python
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule, EDGE_TTS_VOICENAME_MAPPING
from shortGPT.config.languages import Language

# Your custom text
custom_text = """
Your custom content here. 
This text will be spoken in the video.
"""

# Set up voice module
voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.ENGLISH]['male']
voice_module = EdgeTTSVoiceModule(voice_name)

# Create engine
engine = CustomTextShortEngine(
    voiceModule=voice_module,
    custom_text=custom_text,
    background_video_name="your_background_video",
    background_music_name="your_background_music",
    num_images=5,
    watermark="YourChannel",
    language=Language.ENGLISH
)

# Generate video
for step_num, step_info in engine.makeContent():
    print(f"Step {step_num}: {step_info}")

print(f"Video saved to: {engine.get_video_output_path()}")
```

## Benefits

1. **Full Content Control**: Users have complete control over what is said in the video
2. **No LLM Required**: Works without OpenAI or Gemini API keys
3. **Cost Effective**: No API costs for content generation
4. **Consistent Quality**: User controls the exact content quality and style
5. **Custom Messaging**: Perfect for specific announcements, tutorials, or branded content
6. **Same Features**: All existing features still work (images, music, watermarks, etc.)

## Files Modified/Created

### Created:
- `shortGPT/engine/custom_text_short_engine.py` - Main engine implementation
- `test_custom_text_engine.py` - Test script for the new engine
- `demo_custom_text.py` - Demo script showing usage
- `CUSTOM_TEXT_FEATURE_SUMMARY.md` - This documentation

### Modified:
- `gui/ui_tab_short_automation.py` - Updated UI to support custom text input
- `shortGPT/engine/__init__.py` - Added import for new engine

## Testing

The implementation includes comprehensive testing:
- Unit tests for the engine functionality
- Validation of empty text handling
- GUI import verification
- End-to-end demo script

All tests pass successfully, confirming the feature works as expected.

## Future Enhancements

Potential improvements for this feature:
1. **Text Templates**: Pre-made templates for common video types
2. **Text Formatting**: Support for emphasis, pauses, or pronunciation guides
3. **Multi-Language Support**: Enhanced support for different language inputs
4. **Text Statistics**: Show estimated video duration based on text length
5. **Import from File**: Allow importing text content from files (.txt, .docx, etc.)

## Conclusion

The custom text feature successfully extends ShortGPT's capabilities by allowing users to create videos with their own content while maintaining all the powerful automated video generation features. This makes ShortGPT more versatile and accessible to users who want precise control over their video content. 