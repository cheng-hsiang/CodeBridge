#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge GUI - 程式碼簡繁轉換工具 GUI版本
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
import subprocess
import platform
import json
from pathlib import Path
from typing import Optional
import webbrowser

# 添加 src 目錄到 Python 路徑
if hasattr(sys, '_MEIPASS'):
    # PyInstaller 打包後的路徑
    base_path = Path(sys._MEIPASS)
else:
    # 開發環境的路徑
    base_path = Path(__file__).parent

src_path = base_path / 'src'
sys.path.insert(0, str(src_path))

try:
    from src.codebridge import CodeBridge
    from src.config import Config
    CODEBRIDGE_AVAILABLE = True
except ImportError as e:
    CODEBRIDGE_AVAILABLE = False
    IMPORT_ERROR = str(e)


class CodeBridgeGUI:
    """CodeBridge GUI應用程序"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌉 CodeBridge - 程式碼簡繁轉換工具")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # 設置圖標（如果有的話）
        try:
            if hasattr(sys, '_MEIPASS'):
                icon_path = Path(sys._MEIPASS) / 'icon.ico'
                if icon_path.exists():
                    self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        # 變數
        self.project_path = tk.StringVar(value=".")
        self.custom_mappings_path = tk.StringVar()
        self.extensions = tk.StringVar(value=".py,.js,.jsx,.ts,.tsx,.vue,.md,.txt,.json,.yml,.yaml")
        self.preview_mode = tk.BooleanVar(value=True)
        self.create_backup = tk.BooleanVar(value=False)
        self.output_report = tk.StringVar()
        
        # 檢查環境
        self.check_environment()
        
        # 創建界面
        self.create_widgets()
        
        # 居中顯示
        self.center_window()
    
    def check_environment(self):
        """檢查運行環境"""
        self.env_status = {
            'python_version': sys.version,
            'platform': platform.platform(),
            'codebridge_available': CODEBRIDGE_AVAILABLE
        }
        
        if not CODEBRIDGE_AVAILABLE:
            self.env_status['error'] = IMPORT_ERROR
    
    def center_window(self):
        """將窗口居中顯示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """創建界面元件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # 標題
        title_label = ttk.Label(main_frame, text="🌉 CodeBridge", font=("Arial", 16, "bold"))
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 10))
        row += 1
        
        subtitle_label = ttk.Label(main_frame, text="程式碼簡繁轉換工具", font=("Arial", 10))
        subtitle_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # 環境狀態
        if not CODEBRIDGE_AVAILABLE:
            error_frame = ttk.LabelFrame(main_frame, text="❌ 環境檢查", padding="10")
            error_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
            error_frame.columnconfigure(0, weight=1)
            
            error_text = f"CodeBridge 模組載入失敗：\n{IMPORT_ERROR}\n\n請檢查安裝是否正確。"
            error_label = ttk.Label(error_frame, text=error_text, foreground="red")
            error_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
            install_btn = ttk.Button(error_frame, text="嘗試自動修復", command=self.try_fix_environment)
            install_btn.grid(row=1, column=0, pady=(10, 0))
            row += 1
        
        # 專案路徑
        ttk.Label(main_frame, text="專案路徑:").grid(row=row, column=0, sticky=tk.W, pady=5)
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(path_frame, textvariable=self.project_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(path_frame, text="瀏覽", command=self.browse_project_path).grid(row=0, column=1)
        row += 1
        
        # 自定義映射檔案
        ttk.Label(main_frame, text="自定義映射:").grid(row=row, column=0, sticky=tk.W, pady=5)
        custom_frame = ttk.Frame(main_frame)
        custom_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        custom_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(custom_frame, textvariable=self.custom_mappings_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(custom_frame, text="瀏覽", command=self.browse_custom_mappings).grid(row=0, column=1)
        ttk.Button(custom_frame, text="使用內建", command=self.use_builtin_mappings).grid(row=0, column=2, padx=(5, 0))
        row += 1
        
        # 檔案類型
        ttk.Label(main_frame, text="檔案類型:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.extensions).grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        row += 1
        
        # 選項
        options_frame = ttk.LabelFrame(main_frame, text="執行選項", padding="10")
        options_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Checkbutton(options_frame, text="預覽模式（不實際修改檔案）", variable=self.preview_mode).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="創建備份檔案", variable=self.create_backup).grid(row=1, column=0, sticky=tk.W)
        
        # 添加檔名轉換選項
        self.rename_files = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="同時轉換檔案名稱", variable=self.rename_files).grid(row=2, column=0, sticky=tk.W)
        row += 1
        
        # 輸出報告
        ttk.Label(main_frame, text="輸出報告:").grid(row=row, column=0, sticky=tk.W, pady=(15, 5))
        report_frame = ttk.Frame(main_frame)
        report_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(15, 5))
        report_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(report_frame, textvariable=self.output_report).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(report_frame, text="瀏覽", command=self.browse_output_report).grid(row=0, column=1)
        row += 1
        
        # 執行按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(20, 0))
        
        self.run_button = ttk.Button(button_frame, text="🚀 開始轉換", command=self.start_conversion, style="Accent.TButton")
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="💾 儲存配置", command=self.save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📂 載入配置", command=self.load_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❓ 說明", command=self.show_help).pack(side=tk.LEFT)
        row += 1
        
        # 進度條
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 10))
        row += 1
        
        # 日誌輸出
        log_frame = ttk.LabelFrame(main_frame, text="執行日誌", padding="5")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 狀態列
        self.status_var = tk.StringVar(value="準備就緒")
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        status_frame.columnconfigure(0, weight=1)
        
        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, text=f"Python {sys.version.split()[0]} | {platform.system()}").grid(row=0, column=1, sticky=tk.E)
        
        # 初始化日誌
        self.log("🌉 CodeBridge GUI 已啟動")
        if CODEBRIDGE_AVAILABLE:
            self.log("✅ CodeBridge 模組載入成功")
        else:
            self.log("❌ CodeBridge 模組載入失敗")

        # GitHub 資訊區域
        github_frame = ttk.LabelFrame(main_frame, text="📋 GitHub 資訊", padding=10)
        github_frame.grid(row=row+2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        github_info_frame = ttk.Frame(github_frame)
        github_info_frame.pack(fill="x")
        
        # GitHub 倉庫按鈕
        self.github_btn = ttk.Button(
            github_info_frame, 
            text="🔗 查看 GitHub 倉庫",
            command=self.open_github
        )
        self.github_btn.pack(side="left", padx=(0, 10))
        
        # 檢查更新按鈕
        self.update_btn = ttk.Button(
            github_info_frame,
            text="🔄 檢查更新", 
            command=self.check_updates
        )
        self.update_btn.pack(side="left", padx=(0, 10))
        
        # 版本資訊標籤
        self.version_label = ttk.Label(github_info_frame, text="版本: v2.0.0")
        self.version_label.pack(side="right")
    
    def log(self, message: str):
        """添加日誌訊息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message: str):
        """更新狀態列"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def browse_project_path(self):
        """瀏覽專案路徑"""
        path = filedialog.askdirectory(title="選擇專案目錄")
        if path:
            self.project_path.set(path)
    
    def browse_custom_mappings(self):
        """瀏覽自定義映射檔案"""
        path = filedialog.askopenfilename(
            title="選擇自定義映射檔案",
            filetypes=[("文字檔案", "*.txt"), ("所有檔案", "*.*")]
        )
        if path:
            self.custom_mappings_path.set(path)
    
    def use_builtin_mappings(self):
        """使用內建映射"""
        builtin_path = "data/custom_mappings_example.txt"
        if Path(builtin_path).exists():
            self.custom_mappings_path.set(builtin_path)
            self.log(f"✅ 已選擇內建映射檔案: {builtin_path}")
        else:
            messagebox.showwarning("警告", "找不到內建映射檔案")
    
    def browse_output_report(self):
        """瀏覽輸出報告路徑"""
        path = filedialog.asksaveasfilename(
            title="儲存報告檔案",
            defaultextension=".md",
            filetypes=[("Markdown 檔案", "*.md"), ("文字檔案", "*.txt"), ("所有檔案", "*.*")]
        )
        if path:
            self.output_report.set(path)
    
    def try_fix_environment(self):
        """嘗試修復環境"""
        def fix_in_thread():
            try:
                self.log("🔧 嘗試修復環境...")
                self.update_status("修復環境中...")
                
                # 嘗試重新導入
                import importlib
                import sys
                
                # 清除模組快取
                modules_to_remove = [name for name in sys.modules.keys() if name.startswith('src.')]
                for module in modules_to_remove:
                    del sys.modules[module]
                
                # 重新嘗試導入
                global CODEBRIDGE_AVAILABLE
                try:
                    from src.codebridge import CodeBridge
                    from src.config import Config
                    CODEBRIDGE_AVAILABLE = True
                    self.log("✅ 環境修復成功！")
                    messagebox.showinfo("成功", "環境修復成功！請重新啟動應用程序。")
                except ImportError as e:
                    self.log(f"❌ 環境修復失敗: {e}")
                    messagebox.showerror("失敗", f"環境修復失敗：{e}")
                
            except Exception as e:
                self.log(f"❌ 修復過程中發生錯誤: {e}")
                messagebox.showerror("錯誤", f"修復過程中發生錯誤：{e}")
            finally:
                self.update_status("準備就緒")
        
        threading.Thread(target=fix_in_thread, daemon=True).start()
    
    def start_conversion(self):
        """開始轉換"""
        if not CODEBRIDGE_AVAILABLE:
            messagebox.showerror("錯誤", "CodeBridge 模組未正確載入，無法執行轉換。")
            return
        
        # 驗證輸入
        if not self.project_path.get().strip():
            messagebox.showerror("錯誤", "請選擇專案路徑")
            return
        
        if not Path(self.project_path.get()).exists():
            messagebox.showerror("錯誤", "專案路徑不存在")
            return
        
        # 在新線程中執行轉換
        self.run_button.config(state='disabled')
        self.progress.start()
        self.update_status("轉換中...")
        
        def conversion_thread():
            try:
                self.perform_conversion()
            except Exception as e:
                self.log(f"❌ 轉換過程中發生錯誤: {e}")
                messagebox.showerror("錯誤", f"轉換過程中發生錯誤：{e}")
            finally:
                self.progress.stop()
                self.run_button.config(state='normal')
                self.update_status("準備就緒")
        
        threading.Thread(target=conversion_thread, daemon=True).start()
    
    def perform_conversion(self):
        """執行轉換"""
        try:
            # 初始化 CodeBridge
            self.log("🚀 初始化 CodeBridge...")
            codebridge = CodeBridge()
            
            # 載入自定義映射
            if self.custom_mappings_path.get().strip():
                custom_path = self.custom_mappings_path.get().strip()
                if Path(custom_path).exists():
                    self.log(f"📖 載入自定義映射: {custom_path}")
                    count = codebridge.load_custom_mappings(custom_path)
                    self.log(f"✅ 成功載入 {count} 個自定義映射")
                else:
                    self.log(f"⚠️  自定義映射檔案不存在: {custom_path}")
            
            # 處理檔案類型
            file_extensions = None
            if self.extensions.get().strip():
                extensions_str = self.extensions.get().strip()
                file_extensions = set(ext.strip() for ext in extensions_str.split(',') if ext.strip())
                self.log(f"📁 處理檔案類型: {', '.join(sorted(file_extensions))}")
            
            # 執行轉換
            project_path = self.project_path.get().strip()
            preview_mode = self.preview_mode.get()
            
            mode_text = "預覽模式" if preview_mode else "轉換模式"
            self.log(f"⚙️  執行模式: {mode_text}")
            self.log(f"📂 專案路徑: {project_path}")
            
            result = codebridge.convert_project(
                project_path, 
                preview_mode=preview_mode,
                file_extensions=file_extensions
            )
            
            # 生成報告
            report = codebridge.generate_report(result, preview_mode)
            
            # 顯示結果
            self.log("=" * 50)
            for line in report.split('\n'):
                if line.strip():
                    self.log(line)
            self.log("=" * 50)
            
            # 儲存報告
            if self.output_report.get().strip():
                report_path = self.output_report.get().strip()
                try:
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(report)
                    self.log(f"📄 報告已儲存至: {report_path}")
                except Exception as e:
                    self.log(f"❌ 儲存報告失敗: {e}")
            
            # 顯示完成消息
            if result.errors:
                messagebox.showwarning("完成（有錯誤）", f"轉換完成，但發生了 {len(result.errors)} 個錯誤。請查看日誌詳情。")
            else:
                if preview_mode:
                    messagebox.showinfo("預覽完成", f"預覽完成！\n發現 {result.processed_files} 個檔案需要轉換，共 {result.total_conversions} 個字符。")
                else:
                    messagebox.showinfo("轉換完成", f"轉換完成！\n處理了 {result.processed_files} 個檔案，轉換了 {result.total_conversions} 個字符。")
            
        except Exception as e:
            raise Exception(f"轉換失敗: {e}")
    
    def save_config(self):
        """儲存配置"""
        config_data = {
            "project_path": self.project_path.get(),
            "custom_mappings_path": self.custom_mappings_path.get(),
            "extensions": self.extensions.get(),
            "preview_mode": self.preview_mode.get(),
            "create_backup": self.create_backup.get(),
            "output_report": self.output_report.get()
        }
        
        path = filedialog.asksaveasfilename(
            title="儲存配置檔案",
            defaultextension=".json",
            filetypes=[("JSON 檔案", "*.json"), ("所有檔案", "*.*")]
        )
        
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, ensure_ascii=False, indent=2)
                self.log(f"💾 配置已儲存至: {path}")
                messagebox.showinfo("成功", "配置儲存成功！")
            except Exception as e:
                messagebox.showerror("錯誤", f"儲存配置失敗：{e}")
    
    def load_config(self):
        """載入配置"""
        path = filedialog.askopenfilename(
            title="載入配置檔案",
            filetypes=[("JSON 檔案", "*.json"), ("所有檔案", "*.*")]
        )
        
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                self.project_path.set(config_data.get("project_path", "."))
                self.custom_mappings_path.set(config_data.get("custom_mappings_path", ""))
                self.extensions.set(config_data.get("extensions", ".py,.js,.jsx,.ts,.tsx,.vue,.md,.txt,.json,.yml,.yaml"))
                self.preview_mode.set(config_data.get("preview_mode", True))
                self.create_backup.set(config_data.get("create_backup", False))
                self.output_report.set(config_data.get("output_report", ""))
                
                self.log(f"📂 配置已載入: {path}")
                messagebox.showinfo("成功", "配置載入成功！")
            except Exception as e:
                messagebox.showerror("錯誤", f"載入配置失敗：{e}")
    
    def show_help(self):
        """顯示說明"""
        help_text = """
🌉 CodeBridge - 程式碼簡繁轉換工具

【基本使用】
1. 選擇要轉換的專案目錄
2. 可選：選擇自定義映射檔案（或使用內建映射）
3. 設定要處理的檔案類型（用逗號分隔）
4. 選擇執行選項
5. 點擊「開始轉換」

【執行選項】
• 預覽模式：只顯示會被轉換的內容，不實際修改檔案
• 創建備份：轉換前創建原檔案備份

【檔案類型】
支援常見的程式檔案類型，如：
.py, .js, .jsx, .ts, .tsx, .vue, .md, .txt, .json, .yml, .yaml

【自定義映射】
可以載入自定義的簡繁對照檔案，格式：
簡體:繁體 （每行一個映射）

【注意事項】
• 建議先使用預覽模式查看結果
• 重要專案請先備份
• 支援的字庫包含4000+專業術語

更多資訊請參考 README.md
        """
        
        # 創建說明視窗
        help_window = tk.Toplevel(self.root)
        help_window.title("使用說明")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        # 說明文字
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # 關閉按鈕
        btn_frame = ttk.Frame(help_window)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="關閉", command=help_window.destroy).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="查看 GitHub", command=lambda: webbrowser.open("https://github.com/cheng-hsiang/CodeBridge")).pack(side=tk.RIGHT, padx=(0, 10))
    
    def open_github(self):
        """開啟 GitHub 倉庫"""
        webbrowser.open("https://github.com/cheng-hsiang/CodeBridge")
    
    def check_updates(self):
        """檢查更新"""
        try:
            import requests
            response = requests.get("https://api.github.com/repos/cheng-hsiang/CodeBridge/releases/latest", timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['tag_name']
                current_version = "v2.0.0"
                
                if latest_version != current_version:
                    result = messagebox.askyesno(
                        "發現新版本", 
                        f"發現新版本 {latest_version}！\n\n"
                        f"目前版本：{current_version}\n"
                        f"最新版本：{latest_version}\n\n"
                        f"是否前往下載頁面？"
                    )
                    if result:
                        webbrowser.open(f"https://github.com/cheng-hsiang/CodeBridge/releases/tag/{latest_version}")
                else:
                    messagebox.showinfo("版本檢查", f"您已使用最新版本 {current_version}")
            else:
                messagebox.showwarning("檢查更新", "無法連接到 GitHub 檢查更新。")
        except ImportError:
            messagebox.showinfo("缺少依賴", "檢查更新功能需要 requests 模組。\n您可以手動前往 GitHub 查看最新版本。")
        except Exception as e:
            messagebox.showerror("錯誤", f"檢查更新時發生錯誤：{str(e)}")
    
    def run(self):
        """運行GUI應用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


def main():
    """主函數"""
    try:
        app = CodeBridgeGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("嚴重錯誤", f"應用程序啟動失敗：{e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 