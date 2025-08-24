#!/usr/bin/env python3
"""
Claude Code notification sound handler.
Reads configuration from notify.yaml and plays appropriate sound on macOS.
"""

import os
import sys
import subprocess
from pathlib import Path

def play_notification():
    """Play notification sound based on current configuration."""
    # Only run on macOS
    if not sys.platform.startswith('darwin'):
        return

    config = load_config()
    sound_setting = str(config.get('sound_setting', '1'))
    custom_text = config.get('custom_text', 'done')

    try:
        if sound_setting == '0':
            # Silent - do nothing
            pass
        elif sound_setting == '1':
            # Ping - System ding
            subprocess.run(['afplay', '/System/Library/Sounds/Ping.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '2':
            # Glass - Crystal clear sound
            subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '3':
            # Tink - Light chime
            subprocess.run(['afplay', '/System/Library/Sounds/Tink.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '4':
            # Sosumi - Classic bell
            subprocess.run(['afplay', '/System/Library/Sounds/Sosumi.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '5':
            # Pop - Quick pop sound
            subprocess.run(['afplay', '/System/Library/Sounds/Pop.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '6':
            # Blow - Whoosh sound
            subprocess.run(['afplay', '/System/Library/Sounds/Blow.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '7':
            # Hero - Triumphant sound
            subprocess.run(['afplay', '/System/Library/Sounds/Hero.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '8':
            # Basso - Deep bass tone
            subprocess.run(['afplay', '/System/Library/Sounds/Basso.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '9':
            # Bottle - Bottle pop sound
            subprocess.run(['afplay', '/System/Library/Sounds/Bottle.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '10':
            # Frog - Ribbit sound
            subprocess.run(['afplay', '/System/Library/Sounds/Frog.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '11':
            # Funk - Funky bass sound
            subprocess.run(['afplay', '/System/Library/Sounds/Funk.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == '12':
            # Morse - Telegraph beep
            subprocess.run(['afplay', '/System/Library/Sounds/Morse.aiff'],
                         check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == 'say_ready':
            # Text-to-speech "ready"
            subprocess.Popen(['say', 'ready'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == 'say_done':
            # Text-to-speech "done"
            subprocess.Popen(['say', 'done'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sound_setting == 'custom':
            # Custom text-to-speech
            if custom_text:
                subprocess.Popen(['say', custom_text],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        # Silently fail - don't interrupt user workflow
        pass

def load_config():
    """Load notification configuration from YAML file (simple parser)."""
    config_path = Path.home() / ".claude" / "commands" / "notify.yaml"

    # Default configuration
    config = {
        'sound_setting': '1',
        'custom_text': 'done'
    }

    if not config_path.exists():
        return config

    try:
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    config[key] = value
    except Exception as e:
        # Silently use defaults on error
        pass

    return config

if __name__ == '__main__':
    play_notification()
