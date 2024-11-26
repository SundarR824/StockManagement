# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['.', './StockManager'],
    binaries=[],
    datas=[
        ('ui/StockManagement.ui', 'ui/'),
        ('ui/EditStock.ui', 'ui/'),
        ('ui/EditStockGroup.ui', 'ui/'),
        ('ui/StockOperations.ui', 'ui/'),
        ('ui/DeleteStockGroup.ui', 'ui/'),
        ('DBModels/stocks.db', 'DBModels/'),
    ],
    hiddenimports=['PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.uic'],
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
    [],
    exclude_binaries=True,
    name='StockManagementApp',  # Application name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console for GUI application
    icon='resources/stock_management.ico',  # Set custom icon
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StockManagementApp',
)