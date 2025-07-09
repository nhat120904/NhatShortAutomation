# Video Effects Feature for ShortGPT

This document describes the video effects feature that has been added to ShortGPT content engines.

## Overview

The video effects feature allows users to apply visual effects to their videos during the content generation process. This feature is integrated into all content engines and provides a variety of cinematic effects to enhance video content.

## Available Video Effects

### 1. None (Default)
- **Effect**: No visual effect applied
- **Use Case**: When you want to keep the original video quality
- **Parameters**: None

### 2. Sepia Tone
- **Effect**: Classic sepia/vintage photo effect
- **Use Case**: For nostalgic, vintage, or classic themed content
- **Parameters**: None

### 3. Dark Sepia Tone
- **Effect**: Darker sepia effect with adjustable darkness
- **Use Case**: For dramatic, moody vintage content
- **Parameters**:
  - `darkness_factor`: 0.0 (black) to 1.0 (original brightness), default: 0.6

### 4. Darken Video
- **Effect**: Reduces overall brightness of the video
- **Use Case**: For dramatic effect, highlighting text, or moody atmosphere
- **Parameters**:
  - `darkness_factor`: 0.0 (black) to 1.0 (original brightness), default: 0.5

### 5. Vignette Video
- **Effect**: Darkens the edges of the video, creating a tunnel effect
- **Use Case**: To focus attention on the center, create cinematic look
- **Parameters**:
  - `strength`: 0.0 (no effect) to 1.0 (maximum vignette), default: 0.6

## Integration with Content Engines

All content engines now support video effects:

- `ContentShortEngine`
- `CustomTextShortEngine`
- `CustomAudioShortEngine`
- `TextDisplayShortEngine`

## Usage Examples

### Basic Usage

```python
from shortGPT.engine.custom_text_short_engine import CustomTextShortEngine
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.config.languages import Language

voice_module = EdgeTTSVoiceModule("en-US-AriaNeural")

# Create engine with sepia tone effect
engine = CustomTextShortEngine(
    voiceModule=voice_module,
    custom_text="Your video content text here",
    background_video_name="your_video.mp4",
    language=Language.ENGLISH,
    video_effect="sepia_tone",  # Apply sepia effect
    video_effect_params={}      # No additional parameters needed
)
```

### Advanced Usage with Parameters

```python
# Create engine with vignette effect and custom strength
engine = CustomTextShortEngine(
    voiceModule=voice_module,
    custom_text="Your video content text here",
    background_video_name="your_video.mp4",
    language=Language.ENGLISH,
    video_effect="vignette_video",  # Apply vignette effect
    video_effect_params={"strength": 0.8}  # Stronger vignette effect
)
```

### Text Display Engine with Effects

```python
from shortGPT.engine.text_display_short_engine import TextDisplayShortEngine

# Create text display video with darken effect
engine = TextDisplayShortEngine(
    text="Your display text here",
    duration=15,  # 15 seconds
    background_video_name="your_video.mp4",
    video_effect="darken_video",
    video_effect_params={"darkness_factor": 0.6}
)
```

## Implementation Details

### Files Modified/Added

1. **New Files**:
   - `shortGPT/editing_utils/video_effects.py` - Core video effects implementation
   - `shortGPT/editing_framework/editing_steps/apply_video_effect.json` - JSON editing step definition
   - `demo_video_effects.py` - Demo script showing usage
   - `test_video_effects_integration.py` - Test script for verification

2. **Modified Files**:
   - `shortGPT/editing_framework/editing_engine.py` - Added APPLY_VIDEO_EFFECT enum
   - `shortGPT/editing_framework/core_editing_engine.py` - Added video effect processing logic
   - `shortGPT/engine/content_short_engine.py` - Added video effect parameters and rendering
   - `shortGPT/engine/custom_text_short_engine.py` - Added video effect support
   - `shortGPT/engine/custom_audio_short_engine.py` - Added video effect support
   - `shortGPT/engine/text_display_short_engine.py` - Added video effect support
   - `shortGPT/editing_utils/__init__.py` - Added video_effects import

### Technical Architecture

1. **VideoEffect Enum**: Defines available effects in a type-safe manner
2. **Effect Functions**: Individual functions for each effect type (sepia_tone, darken_video, etc.)
3. **apply_video_effect()**: Central function that applies effects based on type and parameters
4. **EditingStep Integration**: New APPLY_VIDEO_EFFECT step in the editing pipeline
5. **Engine Integration**: All engines accept video_effect and video_effect_params parameters

### Effect Processing Flow

1. User specifies `video_effect` and `video_effect_params` when creating content engine
2. Engine stores these parameters in database (`_db_video_effect`, `_db_video_effect_params`)
3. During rendering, if effect is not "none", engine adds APPLY_VIDEO_EFFECT editing step
4. Core editing engine processes the video effect action using MoviePy
5. Effect is applied to the video clip and rendered in final output

## Testing

Run the test script to verify the integration:

```bash
python test_video_effects_integration.py
```

Run the demo script to see examples:

```bash
python demo_video_effects.py
```

## Extending with New Effects

To add new video effects:

1. Add new effect to `VideoEffect` enum in `video_effects.py`
2. Implement the effect function following the existing pattern
3. Update `apply_video_effect()` function to handle the new effect
4. Add parameter information to `get_effect_parameters()` if needed
5. Update `get_video_effect_options()` with user-friendly name

Example:

```python
# In VideoEffect enum
BLUR_EFFECT = "blur_effect"

# New effect function
def blur_video(clip, blur_strength=5):
    def blur_frame(t):
        frame = clip.get_frame(t)
        # Apply blur effect (implementation details)
        return blurred_frame
    
    blurred_clip = VideoClip(blur_frame, duration=clip.duration)
    blurred_clip.fps = clip.fps
    if hasattr(clip, 'audio') and clip.audio:
        blurred_clip = blurred_clip.with_audio(clip.audio)
    return blurred_clip

# Update apply_video_effect()
elif effect == VideoEffect.BLUR_EFFECT:
    blur_strength = kwargs.get('blur_strength', 5)
    return blur_video(clip, blur_strength)
```

## Dependencies

The video effects feature requires:
- MoviePy (already a ShortGPT dependency)
- NumPy (already a ShortGPT dependency)

No additional dependencies are required.

## Performance Considerations

- Video effects are applied during the rendering phase, which may increase processing time
- Effects like vignette and sepia are frame-by-frame operations and can be CPU intensive
- Consider the trade-off between visual quality and processing time when choosing effects
- For production use, test with your typical video lengths and resolutions

## Backward Compatibility

The video effects feature is fully backward compatible:
- Existing content engines continue to work without modification
- Default behavior (no effect) is maintained when video_effect is not specified
- All existing functionality remains unchanged 