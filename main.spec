# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py', '.\\widgets\\alocatMange\\alocatManageSet.py',  '.\\widgets\\alocatMange\\alocatMange.py',
  '.\\widgets\\alocatMange\\armyTransfer.py',  '.\\widgets\\alocatMange\\rocketTransfer.py',  '.\\widgets\\alocatMange\\yearListFor.py',
  ],
             pathex=['G:\\pythonProject\\Equip'],
             binaries=[],
             datas=[],
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
