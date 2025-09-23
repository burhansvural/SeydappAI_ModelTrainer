# debug_version.py - Test version parsing independently

import flet as ft
from importlib.metadata import version


def debug_version_parsing():
    """✅ Debug version parsing - Search results [1] debugging pattern[1]"""
    try:
        flet_version = version('flet')
        print(f"🔍 Raw Flet version: '{flet_version}'")
        print(f"🔍 Type: {type(flet_version)}")

        # ✅ Safe parsing with fallbacks - Search results [1] pattern[1]
        version_parts = flet_version.split('.')
        print(f"🔍 Version parts: {version_parts}")
        print(f"🔍 Parts type: {type(version_parts)}")

        # ✅ Element by element parsing[1]
        for i, part in enumerate(version_parts):
            print(f"🔍 Part [{i}]: '{part}' (type: {type(part)})")
            try:
                int_part = int(part)
                print(f"✅ Converted to int: {int_part}")
            except ValueError as e:
                print(f"❌ Conversion failed: {e}")

        # ✅ Test ControlState
        try:
            test_state = ft.ControlState.HOVERED
            print(f"✅ ControlState available: {test_state}")
        except AttributeError as e:
            print(f"❌ ControlState not available: {e}")

    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_version_parsing()
