# MCS

This project is automation to some game using bridge between [computer / bluestacks] with ADB and Python.

- Used Libs/methods to identify elements: Tesseract / OpenCV / Yolo / Math calculation pixels (from numpy).
- Used Libs to interact: ADB from -> developer.android.com/tools/adb with own custom script to interact. 
- Used Libs to Make GUI: PySide6 and Deigner(for Pyside)


## Features Scripts

- BASE (we has some base can be used in any game with same logic)
- Donate (automatic donate at clan screen)
- Healing (this game has some events who you can kill other account troops, and using that to heal automatic the secondary account)
- Mercenary (You can spend energy to kill those and gain rewards, this will atomatic kill until detect the energy end)
- Lucky Wheel (Inside the game in Ocidental versio, has som lucky wheel, this will play automatic and open just worth patterns)

## Installation
```bash
git clone https://github.com/srmrow/MCS.git

cd MCS

pip install -r requirements.txt

```
- After the git clone go at "Resources/Roleta" and unpack the YoloDetector.pt (the file is splited in 6 parts to can be uploaded at github)


## Recomended Batch example:
```bash
@echo off
cd /d "$YOUR_FOLDERDIR_NAME$\venv\scripts"

call "activate.bat"

cd /d "$YOUR_FOLDERDIR_NAME$"

python main.py language=ENG_US
```


## Usage without GUI
```bash
python main.py GUI=False
```

- default parammeter is with GUI.

## Usage with another language
```bash
python main.py language=Lang_name
```

- lang_name = At folder "Configs/Languages" has json files with the strings, you use same name of the file without the ".json" to switch the language.
- OBS: You can create your own traduction to other language, just need copy the file rename to other language name and translate the strings.


## Contributing

- We not receive helpers in that project, is just study case to improve the owner skills.
- But you are wellcome to send feedback and tips.

Maded by: MS
