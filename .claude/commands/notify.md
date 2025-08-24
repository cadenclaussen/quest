# Notification Sound Command

Configure notification sounds that play when Claude finishes its work.

## Usage

```
/notify [option]
```

## Options

### System Sounds
- `0`, `false`, or `silent` - No sound  
- `1` or `ping` - Ping - System ding sound (default)
- `2` or `glass` - Glass - Crystal clear sound
- `3` or `tink` - Tink - Light chime sound
- `4` or `sosumi` - Sosumi - Classic bell sound
- `5` or `pop` - Pop - Quick pop sound
- `6` or `blow` - Blow - Whoosh sound  
- `7` or `hero` - Hero - Triumphant sound
- `8` or `basso` - Basso - Deep bass tone
- `9` or `bottle` - Bottle - Bottle pop sound
- `10` or `frog` - Frog - Ribbit sound
- `11` or `funk` - Funk - Funky bass sound
- `12` or `morse` - Morse - Telegraph beep

### Text-to-Speech
- `say ready` - Text-to-speech "ready"
- `say done` - Text-to-speech "done"
- `"any text"` - Custom text-to-speech

## Examples

```bash
/notify 0          # Disable sounds
/notify silent     # Disable sounds
/notify 2          # Use glass sound
/notify glass      # Use glass sound
/notify say done   # Use text-to-speech "done"
```

## Implementation

```bash
#!/bin/bash
NOTIFY_CONFIG="$HOME/.claude/commands/notify.yaml"

# Function to get current setting
get_current_setting() {
    if [[ -f "$NOTIFY_CONFIG" ]]; then
        grep "sound_setting:" "$NOTIFY_CONFIG" | awk '{print $2}'
    else
        echo "1"
    fi
}

# Function to update setting
update_setting() {
    local new_setting="$1"
    if [[ -f "$NOTIFY_CONFIG" ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/sound_setting: .*/sound_setting: $new_setting/" "$NOTIFY_CONFIG"
        else
            sed -i "s/sound_setting: .*/sound_setting: $new_setting/" "$NOTIFY_CONFIG"
        fi
    fi
}

# Function to update custom text
update_custom_text() {
    local custom_text="$1"
    if [[ -f "$NOTIFY_CONFIG" ]]; then
        # Remove existing custom_text line if it exists
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' '/^custom_text:/d' "$NOTIFY_CONFIG"
        else
            sed -i '/^custom_text:/d' "$NOTIFY_CONFIG"
        fi
        # Add new custom_text line
        echo "custom_text: $custom_text" >> "$NOTIFY_CONFIG"
    fi
}

# Parse argument
ARG="$1"
NEW_SETTING=""

case "$ARG" in
    "0"|"false"|"silent")
        NEW_SETTING="0"
        echo "🔇 Notification sounds disabled"
        ;;
    "1"|"ping")
        NEW_SETTING="1" 
        echo "🔔 Using Ping sound (default)"
        ;;
    "2"|"glass")
        NEW_SETTING="2"
        echo "🔔 Using Glass sound"
        ;;
    "3"|"tink")
        NEW_SETTING="3"
        echo "🔔 Using Tink sound"
        ;;
    "4"|"sosumi")
        NEW_SETTING="4"
        echo "🔔 Using Sosumi sound"
        ;;
    "5"|"pop")
        NEW_SETTING="5"
        echo "🔔 Using Pop sound"
        ;;
    "6"|"blow")
        NEW_SETTING="6"
        echo "🔔 Using Blow sound"
        ;;
    "7"|"hero")
        NEW_SETTING="7"
        echo "🔔 Using Hero sound"
        ;;
    "8"|"basso")
        NEW_SETTING="8"
        echo "🔔 Using Basso sound"
        ;;
    "9"|"bottle")
        NEW_SETTING="9"
        echo "🔔 Using Bottle sound"
        ;;
    "10"|"frog")
        NEW_SETTING="10"
        echo "🔔 Using Frog sound"
        ;;
    "11"|"funk")
        NEW_SETTING="11"
        echo "🔔 Using Funk sound"
        ;;
    "12"|"morse")
        NEW_SETTING="12"
        echo "🔔 Using Morse sound"
        ;;
    "say ready")
        NEW_SETTING="say_ready"
        echo "🔔 Using text-to-speech 'ready'"
        ;;
    "say done") 
        NEW_SETTING="say_done"
        echo "🔔 Using text-to-speech 'done'"
        ;;
    "")
        echo "Usage: /notify [option]"
        echo ""
        echo "System Sound Options:"
        echo "  0, false, silent - No sound"
        echo "  1, ping          - Ping - System ding (default)"
        echo "  2, glass         - Glass - Crystal clear sound"
        echo "  3, tink          - Tink - Light chime"
        echo "  4, sosumi        - Sosumi - Classic bell"
        echo "  5, pop           - Pop - Quick pop sound"
        echo "  6, blow          - Blow - Whoosh sound"
        echo "  7, hero          - Hero - Triumphant sound"
        echo "  8, basso         - Basso - Deep bass tone"
        echo "  9, bottle        - Bottle - Bottle pop"
        echo "  10, frog         - Frog - Ribbit sound"
        echo "  11, funk         - Funk - Funky bass"
        echo "  12, morse        - Morse - Telegraph beep"
        echo ""
        echo "Text-to-Speech Options:"
        echo "  say ready        - Text-to-speech 'ready'"
        echo "  say done         - Text-to-speech 'done'"
        echo "  \"any text\"       - Custom text-to-speech"
        echo ""
        current=$(get_current_setting)
        echo "Current setting: $current"
        exit 0
        ;;
    *)
        # Custom text-to-speech
        NEW_SETTING="custom"
        update_custom_text "$ARG"
        echo "🔔 Using custom text-to-speech: '$ARG'"
        ;;
esac

# Update the setting
update_setting "$NEW_SETTING"
```