from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

root = Path(SPECPATH)
hiddenimports = collect_submodules('PyQt6')

a = Analysis(
    ['src/app/main.py'],
    pathex=[str(root / 'src')],
    binaries=[],
    datas=[(str(root / 'profiles'), 'profiles')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='single-piece-client', console=False)
app = BUNDLE(exe, name='Single Piece Client.app', icon=None, bundle_identifier='com.yuan2go.singlepiececlient')
coll = COLLECT(app, a.binaries, a.datas, strip=False, upx=False, name='single-piece-client')
