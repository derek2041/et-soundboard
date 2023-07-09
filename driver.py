from threading import Thread
import pyaudio
import wave
import sounddevice as sd
import soundfile as sf
import keyboard
import random

NEED_A_MEDIC = "NEED_A_MEDIC"
REVIVE_ME = "REVIVE_ME"
NEED_AMMO = "NEED_AMMO"
ALLIES = "ALLIES"
AXIS = "AXIS"
NEED_BACKUP = "NEED_BACKUP"
HEAL_ME = "HEAL_ME"
HEAL_THE_SQUAD = "HEAL_THE_SQUAD"
GREAT_SHOT = "GREAT_SHOT"

# TODO: Add support for below
FALL_BACK = "FALL_BACK"
FOLLOW_ME = "FOLLOW_ME"
INCOMING = "INCOMING"
LETS_GO = "LETS_GO"
OOPS = "OOPS"
CHECK_FOR_LANDMINES = "CHECK_FOR_LANDMINES"
CLEAR_THE_MINES = "CLEAR_THE_MINES"
CLEAR_THE_PATH = "CLEAR_THE_PATH"
DEFEND_OUR_OBJECTIVE = "DEFEND_OUR_OBJECTIVE"
ATTACK = "ATTACK"
ALL_CLEAR = "ALL_CLEAR"
HOLD_YOUR_FIRE = "HOLD_YOUR_FIRE"
COVER_ME = "COVER_ME"
NEED_BACKUP = "NEED_BACKUP"
REINFORCE_THE_DEFENSE = "REINFORCE_THE_DEFENSE"
REINFORCE_THE_OFFENSE = "REINFORCE_THE_OFFENSE"
NO = "NO"
YES = "YES"
CELEBRATE = "CELEBRATE"

sound_mappings = {
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
    }
}

def play_mp3_to_mic(mp3_file_path):
    # Open the mp3 file in read mode.
    with wave.open(mp3_file_path, "rb") as wf:
        # Get the audio data from the mp3 file.
        print("wf.getnframes():", wf.getnframes())
        data = wf.readframes(wf.getnframes())
        print("wf.getnchannels()")
        print(wf.getnchannels())
        print("wf.getsampwidth()")
        print(wf.getsampwidth())
        # print("wf.readframes(wf.getnframes())")
        # print(data)

    # Create a PyAudio object.
    pa = pyaudio.PyAudio()

    # Open a stream to the microphone input device.
    stream = pa.open(
        format=pyaudio.get_format_from_width(wf.getsampwidth()),
        channels=1,
        rate=wf.getframerate(),
        # input=True,
        output=True,
    )

    # Write the audio data from the mp3 file to the microphone input stream.
    stream.write(data)

    # Close the stream.
    stream.close()

    # Close the PyAudio object.
    pa.terminate()

def get_device_id(device_name='CABLE Input (VB-Audio Virtual Cable)', samplerate=44100, max_output_channels=2):
    device_data = sd.query_devices()

    for curr in device_data:
        if curr['name'] == device_name \
            and curr['default_samplerate'] == samplerate \
            and curr['max_output_channels'] == max_output_channels:
            return curr['index']
    raise Exception("Could not identify virtual microphone input device.")

def play_audio(filename, device_id):
    try:
        # print("sd.query_devices()")
        # print(sd.query_devices())
        # for device_dict in sd.query_devices():
        #     print("dict for device:")
        #     print(device_dict)
        data, fs = sf.read(filename, dtype='float32')
        # sd.play(data=data, device='Microphone (HD Pro Webcam C920)')
        sd.play(data=data, samplerate=fs, device=device_id)
        sd.wait()
    except Exception as err:
        print(err)
        # sd.play(data, fs)
        # sd.wait()

if __name__ == "__main__":
    # Play the mp3 file to the microphone input source.
    # play_mp3_to_mic("attawaybaby.wav")

    # Main code
    audio_file = 'allies_medic_a.wav'

    """
    {
        'name': 'CABLE Input (VB-Audio Virtual Cable)',
        'index': 15,
        'hostapi': 1,
        'max_input_channels': 0,
        'max_output_channels': 2,
        'default_low_input_latency': 0.0,
        'default_low_output_latency': 0.12,
        'default_high_input_latency': 0.0,
        'default_high_output_latency': 0.24,
        'default_samplerate': 44100.0
    }
    """
    delete_this_later = []
    for voice_line in sound_mappings:
        delete_this_later = delete_this_later + sound_mappings[voice_line][ALLIES] + sound_mappings[voice_line][AXIS]
    print(delete_this_later)
    while True:
        try:
            audio_file_to_play = random.choice(delete_this_later)
            if keyboard.is_pressed('z'):
                virtual_mic_thread = Thread(target=play_audio, kwargs={'filename': audio_file_to_play, 'device_id': get_device_id()})
                speaker_playback_thread = Thread(target=play_audio, kwargs={'filename': audio_file_to_play, 'device_id': get_device_id(device_name='Speakers (Realtek(R) Audio)')})
                virtual_mic_thread.start()
                speaker_playback_thread.start()
                virtual_mic_thread.join()
                speaker_playback_thread.join()
                
                # # Play the audio file through the microphone output
                # play_audio(audio_file_to_play, get_device_id())
                # play_audio(audio_file_to_play, get_device_id(device_name='Speakers (Realtek(R) Audio)'))
        except Exception as err:
            print(err)
            break
