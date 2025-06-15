# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 定義資料檔案
datas = [
    ('src', 'src'),
    ('data', 'data'),
    ('config', 'config'),
    ('examples', 'examples'),
    ('README.md', '.'),
    ('LICENSE', '.'),
]

# 隱藏導入
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'src.codebridge',
    'src.config',
    'src.converter',
    'src.mappings',
    'src.file_processor',
    'src.statistics'
]

a = Analysis(
    ['gui_codebridge.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodeBridge-GUI',
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
    icon=None  # 暫時不使用圖標
) 