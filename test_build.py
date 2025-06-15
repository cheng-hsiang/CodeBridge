#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge 構建測試腳本
快速驗證構建環境和依賴
"""

import sys
import importlib
from pathlib import Path


def test_python_version():
    """測試 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 6):
        print("❌ Python 版本過低，需要 3.6+")
        return False
    else:
        print("✅ Python 版本符合要求")
        return True


def test_required_modules():
    """測試必需的模組"""
    required_modules = [
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'threading',
        'json',
        'pathlib',
        'platform',
        'subprocess'
    ]
    
    print("\n檢查必需模組...")
    all_passed = True
    
    for module_name in required_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            all_passed = False
    
    return all_passed


def test_codebridge_modules():
    """測試 CodeBridge 核心模組"""
    print("\n檢查 CodeBridge 模組...")
    
    # 添加 src 到路徑
    src_path = Path(__file__).parent / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    core_modules = [
        'src.codebridge',
        'src.config',
        'src.converter',
        'src.mappings',
        'src.file_processor',
        'src.statistics'
    ]
    
    all_passed = True
    
    for module_name in core_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            all_passed = False
    
    return all_passed


def test_required_files():
    """測試必需的檔案"""
    print("\n檢查必需檔案...")
    
    required_files = [
        'gui_codebridge.py',
        'codebridge.py',
        'src/codebridge.py',
        'src/config.py',
        'src/converter.py',
        'src/mappings.py',
        'data/custom_mappings_example.txt',
        'README.md'
    ]
    
    all_passed = True
    base_path = Path(__file__).parent
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: 檔案不存在")
            all_passed = False
    
    return all_passed


def test_build_dependencies():
    """測試構建依賴"""
    print("\n檢查構建依賴...")
    
    build_modules = ['pyinstaller']
    
    for module_name in build_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError:
            print(f"⚠️  {module_name}: 未安裝（構建時需要）")


def test_gui_startup():
    """測試 GUI 是否能正常導入"""
    print("\n測試 GUI 模組導入...")
    
    try:
        # 嘗試導入但不實際運行 GUI
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 隱藏窗口
        root.destroy()
        print("✅ tkinter GUI 環境正常")
        return True
    except Exception as e:
        print(f"❌ GUI 環境測試失敗: {e}")
        return False


def run_all_tests():
    """運行所有測試"""
    print("🧪 CodeBridge 構建環境測試")
    print("=" * 40)
    
    tests = [
        ("Python 版本", test_python_version),
        ("必需模組", test_required_modules),
        ("CodeBridge 模組", test_codebridge_modules),
        ("必需檔案", test_required_files),
        ("GUI 環境", test_gui_startup),
        ("構建依賴", test_build_dependencies),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 測試失敗: {e}")
            results.append((test_name, False))
    
    # 顯示總結
    print("\n" + "=" * 40)
    print("📊 測試結果總結:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n通過: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有測試通過！可以開始構建。")
        return True
    else:
        print("⚠️  部分測試未通過，請檢查環境配置。")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 