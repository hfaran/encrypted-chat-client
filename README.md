# encryptedchatthing


## GUI

### Setup

```bash
# Install Kivy from kivy.org
open http://kivy.org/#download
# Install requirements
kivy -m pip install -r requirements.txt
# Install GUI requirements
kivy -m pip install -r gui_requirements.txt
```

### Usage

```bash
kivy gui.py
```


## CLI

### Setup

```bash
# If you use virtualenvwrapper...
mkvirtualenv ect
# Install the requirements
pip install $(cat requirements.txt cli_requirements.txt)
```

### Usage

```bash
./cli.py --help
```
