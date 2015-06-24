# -*- mode: python -*-
import os


a = Analysis(['falloutlauncher.py'],
             pathex=[os.path.dirname(__file__)],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('assets/img/pyFallout3Launcher_Logo.gif', 'assets/img/pyFallout3Launcher_Logo.gif', 'DATA')],
          name='FalloutLauncher.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          )
