# -*- mode: python ; coding: utf-8 -*-

import os
import pyfiglet

# Get the directory where pyfiglet fonts are stored
pyfiglet_fonts_dir = os.path.join(os.path.dirname(pyfiglet.__file__), 'fonts')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('WZORY', 'WZORY'), 
        ('gui_interface/icon.png', 'gui_interface/'),
        (pyfiglet_fonts_dir, os.path.join('pyfiglet', 'fonts'))
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GeneratorListyPrzeszkod',
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
    icon=['gui_interface/icon.png'],
)