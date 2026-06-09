import Quartz
import sys

def callback(proxy, type, event, refcon):
    print("KEY PRESSED!")
    return event

print("Attempting to create Event Tap...")
tap = Quartz.CGEventTapCreate(
    Quartz.kCGSessionEventTap,
    Quartz.kCGHeadInsertEventTap,
    0,
    Quartz.kCGEventMaskForAllEvents,
    callback,
    None
)

if tap is None:
    print("ERROR: FAILED to create Event Tap.")
    print("This confirms macOS is blocking the script.")
    print("\nTo fix this:")
    print(f"1. Open System Settings -> Privacy & Security -> Accessibility")
    print(f"2. Add and Enable this specific file: {sys.executable}")
    print("3. Restart your terminal.")
    sys.exit(1)

print("Event Tap created successfully! Listening for keys (Ctrl+C to stop)...")
loop = Quartz.CFRunLoopGetCurrent()
source = Quartz.CFRunLoopAddSource(loop, tap, Quartz.kCFRunLoopCommonModes)
Quartz.CGEventTapEnable(tap, True)
Quartz.CFRunLoopRun()
