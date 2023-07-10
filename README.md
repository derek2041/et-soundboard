Steps to run/use this soundboard:
`https://vb-audio.com/Cable/` and download the VB Audio Cable driver pack. Run the installer.
`git clone https://github.com/derek2041/et-soundboard.git` to clone this repository.
`cd ./your/path/to/soundboard` to change to the proper directory.
`python -m venv ./venv` to create a new virtual environment.
`.\venv\Scripts\activate` to activate created virtual environment.
`pip install -r requirements.txt` to install all dependencies for the scripts into the freshly created virtual environment.
`python list_devices.py` and identify the names of the virtual input microphone device and your output speaker device. Copy the two names down.

Finally run
`python driver.py --microphone_input_device_name=<the name of your virtual audio cable device as copied down> --speaker_output_device_name=<the name of your spaker device as copied down> --team_config=<ALLIES | AXIS>` to start the soundboard.

Full example command below:
`python driver.py --microphone_input_device_name='CABLE Input (VB-Audio Virtual Cable)' --speaker_output_device_name='Speakers (Realtek(R) Audio)' --team_config=ALLIES`