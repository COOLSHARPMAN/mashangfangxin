# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mashangfangxin.py'],
    pathex=['D:\\py_prj\\ali_kufang', 'D:\\py_prj\\ali_kufang\\topsdk'],
    binaries=[],
    datas=[('config.conf', '.'), ('ui/ui_untitled.py', 'ui')],
    hiddenimports=['topsdk', 'flask'],
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
    name='mashangfangxin',
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
)
