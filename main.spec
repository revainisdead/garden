# -*- mode: python -*-

block_cipher = None

options = [("m", None, "OPTION")]
data_files = [
    ('data/fonts', 'fonts'),
    ('data/graphics', 'graphics'),
    ('data/sounds', 'sounds'),
]


a = Analysis(['src\\main.py'],
             pathex=['C:\\bin\\garden'],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
	  options,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
