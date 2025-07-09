# M3U8 Support in ShortGPT

## Overview
ShortGPT now supports M3U8 playlist files through automatic conversion to MP4 format. This enables processing of streaming video sources that only provide M3U8 playlists while maintaining full compatibility with MoviePy.

## How It Works

### 1. Format Selection Strategy
The yt-dlp configuration now uses a priority-based format selection:
```
MP4 → WebM → Other formats → M3U8 (fallback)
```

This ensures that:
- MP4 and WebM formats are preferred (native MoviePy support)
- M3U8 is used only when other formats aren't available
- Maximum compatibility across different video sources

### 2. Automatic Conversion Process
When an M3U8 file is detected, the following happens automatically:

1. **Detection**: The system identifies M3U8 files by extension
2. **Conversion**: FFmpeg converts M3U8 to MP4 using stream copy (no re-encoding)
3. **Caching**: Converted files are stored in `temp_videos/` with unique names
4. **Processing**: MoviePy processes the converted MP4 file normally

### 3. Conversion Command
```bash
ffmpeg -i input.m3u8 -c copy -avoid_negative_ts make_zero -y output.mp4
```

**Parameters explained:**
- `-c copy`: Copy streams without re-encoding (fast)
- `-avoid_negative_ts make_zero`: Handle timestamp issues
- `-y`: Overwrite existing files

## Key Features

### ✅ Automatic Detection
- No manual intervention required
- Seamlessly integrated into existing workflow
- Works with all ShortGPT content engines

### ✅ Fast Conversion
- Uses stream copy instead of re-encoding
- Significantly faster than transcoding
- Preserves original video quality

### ✅ Intelligent Caching
- Converted files are cached to avoid re-conversion
- Uses MD5 hash for unique naming
- Automatic cleanup of temp files

### ✅ Error Handling
- Timeout protection (5-minute limit)
- Detailed error messages
- Graceful fallback handling

### ✅ Path Safety
- Uses absolute paths throughout
- Prevents working directory issues
- Compatible with the earlier path fixes

## Technical Implementation

### Files Modified

1. **`shortGPT/editing_framework/core_editing_engine.py`**
   - Added `_convert_m3u8_to_mp4()` method
   - Integrated conversion into `process_video_asset()`
   - Added error handling and caching logic

2. **`shortGPT/editing_utils/handle_videos.py`**
   - Updated format selection to include M3U8 as fallback
   - Maintains preference for MP4/WebM formats

3. **Utility Scripts**
   - Updated `cleanup_m3u8_files.py` to reflect new approach
   - Added demo scripts for testing and documentation

### Conversion Method Details

```python
def _convert_m3u8_to_mp4(self, m3u8_path):
    """Convert m3u8 file to mp4 using ffmpeg"""
    # Generate unique output filename
    # Check for existing converted file (caching)
    # Run ffmpeg conversion with error handling
    # Validate output file
    # Return absolute path to converted MP4
```

## Usage Examples

### For Developers
```python
from shortGPT.editing_framework.core_editing_engine import CoreEditingEngine

engine = CoreEditingEngine()

# This will automatically convert M3U8 to MP4 if needed
asset = {
    'type': 'video',
    'parameters': {'url': 'https://example.com/video.m3u8'},
    'actions': []
}

video_clip = engine.process_video_asset(asset)
```

### For End Users
No changes needed! ShortGPT works exactly the same way:
- Create videos through the GUI
- M3U8 files are automatically handled
- No additional configuration required

## Benefits

### 🎯 Expanded Source Support
- Works with streaming platforms that use M3U8
- Supports live stream recordings
- Compatible with adaptive bitrate streams

### 🚀 Performance
- Fast conversion using stream copy
- Minimal processing overhead
- Efficient caching system

### 🔧 Reliability
- Robust error handling
- Timeout protection
- Automatic fallback mechanisms

### 🔄 Backward Compatibility
- All existing functionality preserved
- No breaking changes
- Seamless integration

## Requirements

### System Dependencies
- **FFmpeg 4.0+** (required for M3U8 conversion)
- Python packages already included in ShortGPT

### Verification
Run the demo script to verify setup:
```bash
python demo_m3u8_support.py
```

## Troubleshooting

### Common Issues

1. **FFmpeg Not Found**
   ```
   Error: FFmpeg not found
   Solution: Install FFmpeg and ensure it's in PATH
   ```

2. **Conversion Timeout**
   ```
   Error: M3U8 conversion timed out
   Solution: Check network connection or increase timeout
   ```

3. **Invalid M3U8 File**
   ```
   Error: FFmpeg conversion failed
   Solution: Verify M3U8 URL is accessible and valid
   ```

### Debug Information
Enable verbose logging to see conversion details:
- Conversion attempts are logged to console
- Error messages include FFmpeg output
- File paths and sizes are reported

## Future Enhancements

### Potential Improvements
- Progress tracking for long conversions
- Quality selection for adaptive streams
- Parallel conversion for multiple files
- Integration with video download progress bars

### Configuration Options
Consider adding settings for:
- Conversion timeout limits
- Cache directory location
- Quality preferences for adaptive streams

## Conclusion

The M3U8 support feature significantly expands ShortGPT's capability to work with diverse video sources while maintaining the simplicity and reliability users expect. The automatic conversion approach ensures that users don't need to understand the technical details while developers get a robust, well-integrated solution.

**Key Takeaway**: ShortGPT now works with M3U8 files out of the box - no user action required! 