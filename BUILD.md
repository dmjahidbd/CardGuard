# Building CardGuard Executable

## Creating Windows EXE File

To build a standalone executable for Windows, use PyInstaller:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the EXE

```bash
pyinstaller --name=CardGuard --onefile --windowed --icon=icons/default_icon.ico main.py
```

**Parameters explained:**
- `--name=CardGuard`: Name of the output executable
- `--onefile`: Create a single executable file
- `--windowed`: No console window (GUI only)
- `--icon`: Set custom icon (optional)

### 3. Find Your EXE

After building, find your executable at:
```
dist/CardGuard.exe
```

## Alternative: Using spec file

For more control, create `CardGuard.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icons', 'icons')],  # Include icons folder
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CardGuard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/default_icon.ico'
)
```

Then build with:
```bash
pyinstaller CardGuard.spec
```

## Testing the EXE

1. Navigate to `dist/` folder
2. Run `CardGuard.exe`
3. Test all features
4. Check for any missing dependencies

## Common Issues

**Missing DLLs:**
```bash
pyinstaller --onefile --windowed --hidden-import=PyQt6 main.py
```

**Large file size:**
- Use UPX compression (included in command above)
- Exclude unnecessary packages

**Antivirus false positives:**
- Sign your executable with a code signing certificate
- Submit to antivirus vendors for whitelisting

## Distribution

Once built, upload `CardGuard.exe` to GitHub Releases for public download.
