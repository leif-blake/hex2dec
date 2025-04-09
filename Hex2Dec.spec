# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Create a log of what we're including/excluding for debugging
with open('build/pyinstaller_included_files.txt', 'w') as f:
    f.write("Included Qt files:\n")

# Explicitly exclude the heavy Qt modules
excludes = [
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebChannel",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.Qt3DCore",
    "PySide6.QtMultimedia",
]

# Remove modules from a.pure and a.binaries
for exclude in excludes:
    module_name = exclude.split('.')[-1].lower()

    # Filter binaries
    filtered_binaries = []
    for binary in a.binaries:
        name = binary[0].lower()
        path = binary[1].lower()

        # Skip if it matches excluded module pattern, but keep core files
        if (module_name in name or module_name in path) and 'core' not in name:
            continue
        filtered_binaries.append(binary)

    a.binaries = filtered_binaries

# Make sure we include all platform plugins and essential Qt files
for binary in list(a.binaries):
    name = binary[0].lower()
    if ('platforms' in name or 'styles' in name or 'imageformats' in name or
        'qtcore' in name or 'qtgui' in name or 'qtwidgets' in name or
        name.startswith('qt') or name.endswith('.dll')):
        # Log included Qt files for debugging
        with open('build/pyinstaller_included_files.txt', 'a') as f:
            f.write(f"{binary[0]}\n")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Hex2Dec',
    icon='res/icon256x256.ico',
    debug=True,  # Enable debug information
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Hex2Dec',
)