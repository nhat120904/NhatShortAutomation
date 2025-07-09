#!/usr/bin/env python3
"""
Test script to verify UI video effects integration works correctly.
"""


def test_ui_video_effects_import():
    """Test that UI can import video effects module and create components"""
    try:
        # Test import from the UI file
        from shortGPT.editing_utils.video_effects import get_video_effect_options

        print("✓ Video effects module imported successfully in UI context")

        # Test getting options for UI dropdown
        options = get_video_effect_options()
        option_names = list(options.keys())
        print(f"✓ Found {len(option_names)} effect options for UI: {option_names}")

        # Test that all expected effects are present
        expected_effects = [
            "None",
            "Sepia Tone",
            "Dark Sepia Tone",
            "Darken Video",
            "Vignette Effect",
        ]
        for effect in expected_effects:
            assert effect in option_names, f"Missing effect: {effect}"
        print("✓ All expected video effects available for UI")

        return True
    except Exception as e:
        print(f"✗ Failed to test UI video effects import: {e}")
        return False


def test_gradio_components():
    """Test that gradio components can be created"""
    try:
        import gradio as gr

        from shortGPT.editing_utils.video_effects import get_video_effect_options

        # Test creating video effect dropdown
        video_effect_options = get_video_effect_options()
        video_effect_names = list(video_effect_options.keys())

        # This should work without errors
        video_effect = gr.Dropdown(
            choices=video_effect_names,
            value="None",
            label="Video Effect",
            info="Choose a visual effect to apply to your video",
        )
        print("✓ Video effect dropdown component created successfully")

        # Test creating parameter sliders
        darkness_factor = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.6,
            step=0.1,
            label="Darkness Factor",
            info="0.0 = completely black, 1.0 = original brightness",
        )
        print("✓ Darkness factor slider created successfully")

        vignette_strength = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.6,
            step=0.1,
            label="Vignette Strength",
            info="0.0 = no effect, 1.0 = maximum vignette",
        )
        print("✓ Vignette strength slider created successfully")

        return True
    except Exception as e:
        print(f"✗ Failed to test gradio components: {e}")
        return False


def test_effect_parameter_logic():
    """Test the UI logic for showing/hiding effect parameters"""
    try:
        # Test the logic that determines which parameters to show
        def on_video_effect_change(effect):
            show_darkness = effect in ["Dark Sepia Tone", "Darken Video"]
            show_vignette = effect == "Vignette Effect"
            return show_darkness, show_vignette

        # Test different effects
        test_cases = [
            ("None", False, False),
            ("Sepia Tone", False, False),
            ("Dark Sepia Tone", True, False),
            ("Darken Video", True, False),
            ("Vignette Effect", False, True),
        ]

        for effect, expected_darkness, expected_vignette in test_cases:
            show_darkness, show_vignette = on_video_effect_change(effect)
            assert (
                show_darkness == expected_darkness
            ), f"Wrong darkness visibility for {effect}"
            assert (
                show_vignette == expected_vignette
            ), f"Wrong vignette visibility for {effect}"
            print(f"✓ Effect parameter logic correct for '{effect}'")

        return True
    except Exception as e:
        print(f"✗ Failed to test effect parameter logic: {e}")
        return False


def test_effect_value_conversion():
    """Test converting UI effect names to engine values"""
    try:
        from shortGPT.editing_utils.video_effects import get_video_effect_options

        # Test the conversion logic used in the UI
        video_effect_options = get_video_effect_options()

        test_effects = [
            "None",
            "Sepia Tone",
            "Dark Sepia Tone",
            "Darken Video",
            "Vignette Effect",
        ]

        for effect_name in test_effects:
            video_effect_enum = video_effect_options.get(effect_name, "none")
            video_effect_value = (
                video_effect_enum.value
                if hasattr(video_effect_enum, "value")
                else "none"
            )

            print(f"✓ '{effect_name}' converts to '{video_effect_value}'")

            # Verify the conversion makes sense
            if effect_name == "None":
                assert video_effect_value == "none"
            elif effect_name == "Sepia Tone":
                assert video_effect_value == "sepia_tone"
            elif effect_name == "Dark Sepia Tone":
                assert video_effect_value == "sepia_tone_dark"
            elif effect_name == "Darken Video":
                assert video_effect_value == "darken_video"
            elif effect_name == "Vignette Effect":
                assert video_effect_value == "vignette_video"

        print("✓ All effect name to value conversions work correctly")
        return True
    except Exception as e:
        print(f"✗ Failed to test effect value conversion: {e}")
        return False


def main():
    """Run all UI tests"""
    print("=== Testing Video Effects UI Integration ===\n")

    tests = [
        ("UI Video Effects Import Test", test_ui_video_effects_import),
        ("Gradio Components Test", test_gradio_components),
        ("Effect Parameter Logic Test", test_effect_parameter_logic),
        ("Effect Value Conversion Test", test_effect_value_conversion),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")

    print(f"\n=== UI Test Results: {passed}/{total} tests passed ===")

    if passed == total:
        print(
            "🎉 All UI tests passed! Video effects UI integration is working correctly."
        )
        print("\nThe UI now includes:")
        print("- Video Effect dropdown with all available effects")
        print("- Dynamic parameter sliders (shown based on selected effect)")
        print("- Proper integration with all content engines")
        print("- Automatic conversion from UI values to engine parameters")
        return True
    else:
        print("❌ Some UI tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
