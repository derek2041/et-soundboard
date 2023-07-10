from threading import Thread
import sounddevice as sd
import soundfile as sf
import keyboard
import random
import sys

ALLIES = "ALLIES"
AXIS = "AXIS"

TEAM_CONFIG_FLAG = "--team_config"
TEAM_CONFIG = "TEAM_CONFIG"
MICROPHONE_INPUT_DEVICE_NAME_FLAG = "--microphone_input_device_name"
MICROPHONE_INPUT_DEVICE_NAME = "MICROPHONE_INPUT_DEVICE_NAME"
SPEAKER_OUTPUT_DEVICE_NAME_FLAG = "--speaker_output_device_name"
SPEAKER_OUTPUT_DEVICE_NAME = "SPEAKER_OUTPUT_DEVICE_NAME"
MICROPHONE_INPUT_SAMPLE_RATE_FLAG = "--microphone_input_sample_rate"
MICROPHONE_INPUT_SAMPLE_RATE = "MICROPHONE_INPUT_SAMPLE_RATE"
SPEAKER_OUTPUT_SAMPLE_RATE_FLAG = "--speaker_output_sample_rate"
SPEAKER_OUTPUT_SAMPLE_RATE = "SPEAKER_OUTPUT_SAMPLE_RATE"
MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS_FLAG = "--microphone_input_max_output_channels"
MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS = "MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS"
SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS_FLAG = "--speaker_output_max_output_channels"
SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS = "SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS"

# These voice lines are loaded and supported but not necessarily used.
# Check KEY_BINDINGS to make sure there is a mapping bound for this sound
# to use it.
NEED_A_MEDIC = "NEED_A_MEDIC"
REVIVE_ME = "REVIVE_ME"
NEED_AMMO = "NEED_AMMO"
NEED_BACKUP = "NEED_BACKUP"
HEAL_ME = "HEAL_ME"
HEAL_THE_SQUAD = "HEAL_THE_SQUAD"
GREAT_SHOT = "GREAT_SHOT"
NO = "NO"
YES = "YES"
CELEBRATE = "CELEBRATE"
CHECK_FOR_LANDMINES = "CHECK_FOR_LANDMINES"
DEFEND_OUR_OBJECTIVE = "DEFEND_OUR_OBJECTIVE"
ATTACK = "ATTACK"
THANK_YOU = "THANK_YOU"
NO_PROBLEM = "NO_PROBLEM"

# TODO: Add support for below
FALL_BACK = "FALL_BACK"
FOLLOW_ME = "FOLLOW_ME"
INCOMING = "INCOMING"
LETS_GO = "LETS_GO"
OOPS = "OOPS"
CLEAR_THE_MINES = "CLEAR_THE_MINES"
CLEAR_THE_PATH = "CLEAR_THE_PATH"
ALL_CLEAR = "ALL_CLEAR"
HOLD_YOUR_FIRE = "HOLD_YOUR_FIRE"
COVER_ME = "COVER_ME"
REINFORCE_THE_DEFENSE = "REINFORCE_THE_DEFENSE"
REINFORCE_THE_OFFENSE = "REINFORCE_THE_OFFENSE"

SOUND_MAPPINGS = {
    NEED_A_MEDIC: {
        ALLIES: ["allies_medic_a.wav", "allies_medic_b.wav", "allies_medic_c.wav"],
        AXIS: ["axis_medic_a.wav", "axis_medic_b.wav", "axis_medic_c.wav"]
    },
    REVIVE_ME: {
        ALLIES: ["allies_revive_a.wav", "allies_revive_b.wav"],
        AXIS: ["axis_revive_a.wav", "axis_revive_b.wav"]
    },
    NEED_AMMO: {
        ALLIES: ["allies_need_ammo.wav"],
        AXIS: ["axis_need_ammo.wav"]
    }, 
    NEED_BACKUP: {
        ALLIES: ["allies_need_backup_a.wav", "allies_need_backup_b.wav"],
        AXIS: ["axis_need_backup_a.wav", "axis_need_backup_b.wav"]
    },
    HEAL_ME: {
        ALLIES: ["allies_heal_me_a.wav"],
        AXIS: ["axis_heal_me_a.wav", "axis_heal_me_b.wav"]
    },
    HEAL_THE_SQUAD: {
        ALLIES: ["allies_heal_the_squad_a.wav", "allies_heal_the_squad_b.wav"],
        AXIS: ["axis_heal_the_squad_a.wav", "axis_heal_the_squad_b.wav"]
    },
    GREAT_SHOT: {
        ALLIES: ["allies_great_shot_a.wav", "allies_great_shot_b.wav"],
        AXIS: ["axis_great_shot_a.wav", "axis_great_shot_b.wav"]
    },
    NO: {
        ALLIES: ["allies_no_a.wav", "allies_no_b.wav", "allies_no_c.wav", "allies_no_d.wav", "allies_no_e.wav", "allies_no_f.wav"],
        AXIS: ["axis_no_a.wav", "axis_no_b.wav", "axis_no_c.wav"]
    },
    YES: {
        ALLIES: ["allies_yes_a.wav", "allies_yes_b.wav", "allies_yes_c.wav"],
        AXIS: ["axis_yes_a.wav", "axis_yes_b.wav"]
    },
    CELEBRATE: {
        ALLIES: [
            "allies_celebrate_a.wav", "allies_celebrate_b.wav", "allies_celebrate_c.wav",
            "allies_celebrate_d.wav", "allies_celebrate_e.wav", "allies_celebrate_f.wav",
            "allies_celebrate_g.wav", "allies_celebrate_h.wav", "allies_celebrate_i.wav"
        ],
        AXIS: [
            "axis_celebrate_a.wav", "axis_celebrate_b.wav", "axis_celebrate_c.wav",
            "axis_celebrate_d.wav", "axis_celebrate_e.wav", "axis_celebrate_f.wav",
            "axis_celebrate_g.wav", "axis_celebrate_h.wav", "axis_celebrate_i.wav"
        ]
    },
    ATTACK: {
        ALLIES: ["allies_attack_a.wav", "allies_attack_b.wav"],
        AXIS: ["axis_attack_a.wav", "axis_attack_b.wav", "axis_attack_c.wav"]
    },
    DEFEND_OUR_OBJECTIVE: {
        ALLIES: ["allies_defend_a.wav", "allies_defend_b.wav"],
        AXIS: ["axis_defend_a.wav", "axis_defend_b.wav"]
    },
    CHECK_FOR_LANDMINES: {
        ALLIES: ["allies_check_for_mines_a.wav"],
        AXIS: ["axis_check_for_mines_a.wav", "axis_check_for_mines_b.wav"]
    },
    THANK_YOU: {
        ALLIES: ["allies_thank_you_a.wav", "allies_thank_you_b.wav", "allies_thank_you_c.wav", "allies_thank_you_d.wav"],
        AXIS: ["axis_thank_you_a.wav", "axis_thank_you_b.wav", "axis_thank_you_c.wav"]
    },
    NO_PROBLEM: {
        ALLIES: ["allies_no_problem_a.wav", "allies_no_problem_b.wav", "allies_no_problem_c.wav", "allies_no_problem_d.wav"],
        AXIS: ["axis_no_problem_a.wav"]
    }
}

KEY_BINDINGS = {
    'v+1': NEED_A_MEDIC,
    'v+2': REVIVE_ME,
    'v+3': CELEBRATE,
    'v+4': YES,
    'v+5': NO,
    'v+6': GREAT_SHOT,
    'v+7': NEED_BACKUP,
    'v+8': ATTACK,
    'v+9': THANK_YOU,
    'v+0': NO_PROBLEM
}

AUDIO_PLAYER_CONFIG = {
    TEAM_CONFIG: ALLIES, # Allies by default
    MICROPHONE_INPUT_DEVICE_NAME: None,
    SPEAKER_OUTPUT_DEVICE_NAME: None,
    MICROPHONE_INPUT_SAMPLE_RATE: 44100,
    SPEAKER_OUTPUT_SAMPLE_RATE: 44100,
    MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS: 2,
    SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS: 2
}

def get_device_id(device_name, samplerate=44100, max_output_channels=2):
    if device_name is None or device_name == '':
        raise Exception("Device name must be specified via cmd line flags.")
    
    device_data = sd.query_devices()

    for curr in device_data:
        if curr['name'] == device_name \
            and curr['default_samplerate'] == samplerate \
            and curr['max_output_channels'] == max_output_channels:
            return curr['index']
    raise Exception("Could not identify virtual microphone input device.")

def play_audio_callback(voice_line):
    audio_file_pool = SOUND_MAPPINGS[voice_line][AUDIO_PLAYER_CONFIG[TEAM_CONFIG]]
    audio_file_to_play = random.choice(audio_file_pool)

    virtual_mic_thread = Thread(
        target=play_audio,
        kwargs={
            'filename': audio_file_to_play,
            'device_id': get_device_id(
                device_name=AUDIO_PLAYER_CONFIG[MICROPHONE_INPUT_DEVICE_NAME],
                samplerate=AUDIO_PLAYER_CONFIG[MICROPHONE_INPUT_SAMPLE_RATE],
                max_output_channels=AUDIO_PLAYER_CONFIG[MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS]
            )
        }
    )
    speaker_playback_thread = Thread(
        target=play_audio,
        kwargs={
            'filename': audio_file_to_play,
            'device_id': get_device_id(
                device_name=AUDIO_PLAYER_CONFIG[SPEAKER_OUTPUT_DEVICE_NAME],
                samplerate=AUDIO_PLAYER_CONFIG[SPEAKER_OUTPUT_SAMPLE_RATE],
                max_output_channels=AUDIO_PLAYER_CONFIG[SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS]
            )
        }
    )

    virtual_mic_thread.start()
    speaker_playback_thread.start()
    
    virtual_mic_thread.join()
    speaker_playback_thread.join()

def play_audio(filename, device_id):
    try:
        data, fs = sf.read(filename, dtype='float32')
        sd.play(data=data, samplerate=fs, device=device_id)
        sd.wait()
    except Exception as err:
        print(err)

if __name__ == "__main__":    
    params = sys.argv[1:]

    for param in params:
        if param.startswith(TEAM_CONFIG_FLAG):
            AUDIO_PLAYER_CONFIG[TEAM_CONFIG] = param.split("=")[1]

        if param.startswith(MICROPHONE_INPUT_DEVICE_NAME_FLAG):
            AUDIO_PLAYER_CONFIG[MICROPHONE_INPUT_DEVICE_NAME] = param.split("=")[1]

        if param.startswith(SPEAKER_OUTPUT_DEVICE_NAME_FLAG):
            AUDIO_PLAYER_CONFIG[SPEAKER_OUTPUT_DEVICE_NAME] = param.split("=")[1]

        if param.startswith(MICROPHONE_INPUT_SAMPLE_RATE_FLAG):
            AUDIO_PLAYER_CONFIG[MICROPHONE_INPUT_SAMPLE_RATE] = param.split("=")[1]

        if param.startswith(SPEAKER_OUTPUT_SAMPLE_RATE_FLAG):
            AUDIO_PLAYER_CONFIG[SPEAKER_OUTPUT_SAMPLE_RATE] = param.split("=")[1]

        if param.startswith(MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS_FLAG):
            AUDIO_PLAYER_CONFIG[MICROPHONE_INPUT_MAX_OUTPUT_CHANNELS] = param.split("=")[1]

        if param.startswith(SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS_FLAG):
            AUDIO_PLAYER_CONFIG[SPEAKER_OUTPUT_MAX_OUTPUT_CHANNELS] = param.split("=")[1]

    for key_combo, voice_line in KEY_BINDINGS.items():
        keyboard.add_hotkey(hotkey=key_combo, callback=play_audio_callback, args=(voice_line,))

    keyboard.wait()
