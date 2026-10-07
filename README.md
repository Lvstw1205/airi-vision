# AIRI Vision

### Local AI Camera & Gesture Recognition

Local camera intelligence with MediaPipe hand landmarks, OpenCV face enrollment and Ollama visual Q&A. Privacy-focused, independently installable, noncommercial source release.

**Community source release · v0.1.0 · Python 3.11+ · Personal and noncommercial use**

## What it does

- Browser camera selection with visible start and stop controls.
- Local 21-point hand landmarks and joint-based gesture classification.
- YuNet face detection and SFace comparison against locally enrolled samples.
- Three-sample enrollment, explicit deletion and no background recording.
- Single-frame visual questions through a local vision-capable Ollama model.
- Verified model downloads, loopback HTTP and per-session request tokens.

## Quick start

macOS is the primary tested platform. Install Python 3.11+ and Git first. On Windows,
the standalone Vision/Stock101 Python host may run, but Windows packaging is not verified.
AIRI Assistant and Tim Works contain macOS/POSIX integrations.

```bash
git clone https://github.com/Lvstw1205/airi-vision.git
cd airi-vision
bash scripts/setup.sh
.venv/bin/python run.py
```

Open **http://127.0.0.1:8768** in your browser. On macOS you can also double-click
`Start.command` after downloading and extracting the source archive.

After installing Python dependencies, download the public inference models:

```bash
.venv/bin/python scripts/download_vision_models.py
```

Start the app, click **Start camera**, and allow camera access. Toggle **Face comparison**
or enroll a consenting participant. For image questions, start [Ollama](https://ollama.com/),
install a vision-capable model such as `llava`, refresh the model list and analyze one frame.
Text-only models are rejected. Cloud-routed Ollama models are not used for frames.

Recognition is for personalization, not authentication. Camera accuracy depends on lighting,
distance and the model. Human face accuracy has not been benchmarked by this release.

## Data and operation

Your records are created in `data/`; downloaded models use `.runtime/` or `web/hand-assets/`.
These paths are excluded from Git. Nothing from the original owner's accounts, recordings,
conversations, credentials, face enrollments or trading ledgers is included.

The service runs while its Python process and computer are awake. Closing the browser does
not stop the server. Optional macOS login startup is installed with
`.venv/bin/python scripts/install_autostart.py`; use `--remove` to uninstall that launcher.
This is login startup, not execution while powered off. Keep the extracted folder in place.

## Documentation

- [한국어 시작 안내](README.ko.md)
- [Setup and troubleshooting](docs/SETUP.md)
- [Privacy and data handling](PRIVACY.md)
- [Security reporting](SECURITY.md)
- [Release validation](docs/VALIDATION.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## License

Original code is **source-available under [PolyForm Noncommercial 1.0.0](LICENSE.md)**.
Personal and noncommercial use, modification and redistribution are subject to those terms.
Commercial use requires separate permission from the rights holder. This is not an
OSI-approved open-source license. Third-party code and models retain their own licenses.
Required attribution is in [NOTICE](NOTICE).

## Related projects

[AIRI Assistant](https://github.com/Lvstw1205/airi-assistant) ·
[AIRI Vision](https://github.com/Lvstw1205/airi-vision) ·
[Stock101](https://github.com/Lvstw1205/stock101) ·
[AIRI Playbook](https://github.com/Lvstw1205/airi-playbook) ·
[Tim Works Beta](https://github.com/Lvstw1205/tim-works-beta)
