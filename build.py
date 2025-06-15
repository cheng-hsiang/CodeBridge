#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge 自動化構建腳本
用於構建 Windows exe 執行檔
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path
import argparse


class CodeBridgeBuilder:
    """CodeBridge 構建器"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / 'dist'
        self.build_dir = self.root_dir / 'build'
        self.version = self.get_version()
    
    def get_version(self):
        """獲取版本號"""
        try:
            # 從 setup.py 或其他地方獲取版本
            return "2.0.0"
        except:
            return "dev"
    
    def check_environment(self):
        """檢查構建環境"""
        print("🔍 檢查構建環境...")
        
        # 檢查 Python 版本
        python_version = sys.version_info
        print(f"   Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 6):
            raise RuntimeError("需要 Python 3.6 或更高版本")
        
        # 檢查作業系統
        system = platform.system()
        print(f"   作業系統: {system}")
        
        # 檢查必要的檔案
        required_files = [
            'gui_codebridge.py',
            'src/codebridge.py',
            'src/config.py',
            'codebridge.spec'
        ]
        
        for file_path in required_files:
            if not (self.root_dir / file_path).exists():
                raise FileNotFoundError(f"找不到必要檔案: {file_path}")
        
        print("✅ 環境檢查通過")
    
    def install_dependencies(self):
        """安裝構建依賴"""
        print("📦 安裝構建依賴...")
        
        try:
            # 安裝 PyInstaller
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'build_requirements.txt'
            ], check=True)
            
            print("✅ 依賴安裝完成")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"依賴安裝失敗: {e}")
    
    def clean_build(self):
        """清理構建目錄"""
        print("🧹 清理構建目錄...")
        
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   已刪除: {dir_path}")
    
    def create_icon(self):
        """創建應用程序圖標"""
        print("🎨 準備應用程序圖標...")
        
        icon_path = self.root_dir / 'icon.ico'
        if not icon_path.exists():
            # 如果沒有圖標，創建一個簡單的文字版本
            print("   未找到 icon.ico，將使用預設圖標")
        else:
            print(f"   使用圖標: {icon_path}")
    
    def build_exe(self, console=False):
        """構建 exe 檔案"""
        print("🔨 開始構建 exe...")
        
        try:
            # 使用 PyInstaller 構建
            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--clean',
                '--noconfirm',
                'codebridge.spec'
            ]
            
            if console:
                # 如果需要控制台版本（除錯用）
                cmd.extend(['--console'])
            
            subprocess.run(cmd, check=True, cwd=self.root_dir)
            
            print("✅ exe 構建完成")
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"構建失敗: {e}")
    
    def create_installer(self):
        """創建安裝程序"""
        print("📦 準備發布檔案...")
        
        # 檢查構建產物
        exe_path = self.dist_dir / 'CodeBridge-GUI.exe'
        if not exe_path.exists():
            raise FileNotFoundError("找不到構建的 exe 檔案")
        
        # 創建發布目錄
        release_dir = self.root_dir / f'release-{self.version}'
        if release_dir.exists():
            shutil.rmtree(release_dir)
        release_dir.mkdir()
        
        # 複製主要檔案
        shutil.copy2(exe_path, release_dir / 'CodeBridge-GUI.exe')
        
        # 複製文件
        for doc_file in ['README.md', 'LICENSE']:
            src_file = self.root_dir / doc_file
            if src_file.exists():
                shutil.copy2(src_file, release_dir / doc_file)
        
        # 複製範例配置
        examples_dir = release_dir / 'examples'
        examples_dir.mkdir(exist_ok=True)
        
        if (self.root_dir / 'data' / 'custom_mappings_example.txt').exists():
            shutil.copy2(
                self.root_dir / 'data' / 'custom_mappings_example.txt',
                examples_dir / 'custom_mappings_example.txt'
            )
        
        # 創建使用說明
        usage_guide = release_dir / 'USAGE.txt'
        with open(usage_guide, 'w', encoding='utf-8') as f:
            f.write("""🌉 CodeBridge GUI 使用說明

【快速開始】
1. 執行 CodeBridge-GUI.exe
2. 選擇要轉換的專案目錄
3. 可選：載入自定義映射檔案 (examples/custom_mappings_example.txt)
4. 建議先使用「預覽模式」查看轉換結果
5. 確認無誤後關閉預覽模式，重新執行實際轉換

【注意事項】
• 重要專案請先備份
• 首次使用建議使用預覽模式
• 支援多種程式語言檔案
• 內建4000+專業術語字庫

【自定義映射格式】
檔案格式：每行一個映射，用冒號分隔
範例：
简体字:繁體字
项目:專案
接口:介面

【技術支援】
如有問題請查看 README.md 或聯繫開發者
""")
        
        print(f"✅ 發布檔案準備完成: {release_dir}")
        
        # 創建 ZIP 檔案
        zip_path = self.root_dir / f'CodeBridge-GUI-{self.version}-windows.zip'
        shutil.make_archive(str(zip_path.with_suffix('')), 'zip', release_dir)
        
        print(f"📦 發布包已創建: {zip_path}")
        
        return zip_path
    
    def test_exe(self):
        """測試構建的 exe"""
        print("🧪 測試 exe...")
        
        exe_path = self.dist_dir / 'CodeBridge-GUI.exe'
        if not exe_path.exists():
            raise FileNotFoundError("找不到構建的 exe 檔案")
        
        # 這裡可以添加自動化測試
        print("   手動測試：請運行生成的 exe 檔案檢查功能")
        print(f"   exe 位置: {exe_path}")
    
    def build_all(self, clean=True, test=True):
        """完整構建流程"""
        try:
            print("🌉 CodeBridge GUI 構建開始")
            print("=" * 50)
            
            # 檢查環境
            self.check_environment()
            
            # 安裝依賴
            self.install_dependencies()
            
            # 清理構建目錄
            if clean:
                self.clean_build()
            
            # 準備圖標
            self.create_icon()
            
            # 構建 exe
            self.build_exe()
            
            # 創建發布包
            zip_path = self.create_installer()
            
            # 測試
            if test:
                self.test_exe()
            
            print("\n" + "=" * 50)
            print("🎉 構建完成！")
            print(f"📦 發布包: {zip_path}")
            print("\n💡 下一步:")
            print("1. 測試生成的 exe 檔案")
            print("2. 將發布包上傳到 GitHub Releases")
            print("3. 更新版本標籤和發布說明")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 構建失敗: {e}")
            return False


def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='CodeBridge 構建工具')
    parser.add_argument('--no-clean', action='store_true', help='不清理構建目錄')
    parser.add_argument('--no-test', action='store_true', help='不運行測試')
    parser.add_argument('--console', action='store_true', help='構建控制台版本（除錯用）')
    
    args = parser.parse_args()
    
    builder = CodeBridgeBuilder()
    
    success = builder.build_all(
        clean=not args.no_clean,
        test=not args.no_test
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 