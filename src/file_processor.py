#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 檔案處理器
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
import logging


@dataclass
class FileProcessResult:
    """檔案處理結果"""
    file_path: str
    processed: bool = False
    conversions: int = 0
    error: Optional[str] = None
    preview_data: List[Tuple[str, str, int]] = None
    
    def __post_init__(self):
        if self.preview_data is None:
            self.preview_data = []


class FileProcessor:
    """
    檔案處理器
    
    負責處理各種類型的檔案
    """
    
    def __init__(self, config):
        """
        初始化檔案處理器
        
        Args:
            config: 配置對象
        """
        self.config = config
        self.logger = logging.getLogger('CodeBridge.FileProcessor')
    
    def process_file(self, file_path: Path, converter, preview_mode: bool = False) -> FileProcessResult:
        """
        處理單個檔案
        
        Args:
            file_path: 檔案路徑
            converter: 轉換器實例
            preview_mode: 預覽模式
        
        Returns:
            FileProcessResult: 處理結果
        """
        result = FileProcessResult(file_path=str(file_path))
        
        try:
            # 檢查檔案是否可讀
            if not file_path.is_file() or not os.access(file_path, os.R_OK):
                result.error = "檔案不存在或無法讀取"
                return result
            
            # 檢查檔案大小
            file_size = file_path.stat().st_size
            if file_size > self.config.max_file_size:
                result.error = f"檔案過大 ({file_size} bytes > {self.config.max_file_size} bytes)"
                return result
            
            # 讀取檔案內容
            content = self._read_file_content(file_path)
            if content is None:
                result.error = "無法讀取檔案內容"
                return result
            
            if preview_mode:
                # 預覽模式：只分析不修改
                preview_conversions = converter.preview_conversion(content)
                result.preview_data = preview_conversions
                result.conversions = sum(count for _, _, count in preview_conversions)
                
                if preview_conversions:
                    self.logger.debug(f"📋 {file_path.name}: 預覽 {len(preview_conversions)} 個轉換")
                    for simplified, traditional, count in preview_conversions[:5]:  # 只記錄前5個
                        self.logger.debug(f"  • '{simplified}' → '{traditional}' ({count} 次)")
            else:
                # 轉換模式：實際修改檔案
                converted_content, conversion_count = converter.convert_text(content)
                
                if conversion_count > 0:
                    # 寫回檔案
                    success = self._write_file_content(file_path, converted_content)
                    if success:
                        result.processed = True
                        result.conversions = conversion_count
                        self.logger.info(f"✅ {file_path.name}: 轉換了 {conversion_count} 個字符")
                    else:
                        result.error = "寫入檔案失敗"
            
        except Exception as e:
            result.error = str(e)
            self.logger.error(f"❌ 處理檔案 {file_path.name} 時發生錯誤: {e}")
        
        return result
    
    def _read_file_content(self, file_path: Path) -> Optional[str]:
        """
        讀取檔案內容，自動處理編碼
        
        Args:
            file_path: 檔案路徑
        
        Returns:
            Optional[str]: 檔案內容，失敗時返回None
        """
        # 嘗試不同的編碼
        encodings = ['utf-8', 'utf-8-sig', 'gb2312', 'gbk', 'big5', 'latin1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                self.logger.debug(f"成功使用 {encoding} 編碼讀取 {file_path.name}")
                return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.logger.warning(f"讀取檔案 {file_path.name} 時發生錯誤: {e}")
                break
        
        # 如果所有編碼都失敗，嘗試忽略錯誤
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            self.logger.warning(f"使用 utf-8 編碼忽略錯誤讀取 {file_path.name}")
            return content
        except Exception as e:
            self.logger.error(f"無法讀取檔案 {file_path.name}: {e}")
            return None
    
    def _write_file_content(self, file_path: Path, content: str) -> bool:
        """
        寫入檔案內容
        
        Args:
            file_path: 檔案路徑
            content: 要寫入的內容
        
        Returns:
            bool: 是否寫入成功
        """
        try:
            # 備份原檔案（如果啟用）
            if self.config.create_backup:
                self._create_backup(file_path)
            
            # 寫入檔案
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.debug(f"成功寫入檔案 {file_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"寫入檔案 {file_path.name} 失敗: {e}")
            return False
    
    def _create_backup(self, file_path: Path) -> bool:
        """
        創建檔案備份
        
        Args:
            file_path: 原檔案路徑
        
        Returns:
            bool: 是否備份成功
        """
        try:
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            
            # 如果備份檔案已存在，添加時間戳
            if backup_path.exists():
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = file_path.with_suffix(f".{timestamp}.backup")
            
            # 複製檔案
            import shutil
            shutil.copy2(file_path, backup_path)
            
            self.logger.debug(f"創建備份: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.warning(f"創建備份失敗 {file_path.name}: {e}")
            return False
    
    def is_text_file(self, file_path: Path) -> bool:
        """
        判斷是否為文字檔案
        
        Args:
            file_path: 檔案路徑
        
        Returns:
            bool: 是否為文字檔案
        """
        try:
            # 檢查副檔名
            if file_path.suffix.lower() in self.config.target_extensions:
                return True
            
            # 檢查檔案內容
            with open(file_path, 'rb') as f:
                chunk = f.read(512)
            
            # 簡單的二進位檔案檢測
            if b'\x00' in chunk:
                return False
            
            # 嘗試解碼為文字
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                return False
                
        except Exception:
            return False
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        獲取檔案資訊
        
        Args:
            file_path: 檔案路徑
        
        Returns:
            dict: 檔案資訊
        """
        try:
            stat = file_path.stat()
            return {
                'path': str(file_path),
                'name': file_path.name,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'extension': file_path.suffix,
                'is_text': self.is_text_file(file_path)
            }
        except Exception as e:
            return {
                'path': str(file_path),
                'error': str(e)
            }
    
    def scan_directory(self, directory: Path) -> List[Path]:
        """
        掃描目錄中的所有符合條件的檔案
        
        Args:
            directory: 目錄路徑
        
        Returns:
            List[Path]: 符合條件的檔案列表
        """
        files = []
        
        try:
            for file_path in directory.rglob('*'):
                if not file_path.is_file():
                    continue
                
                # 檢查是否在排除目錄中
                if any(part in self.config.exclude_dirs for part in file_path.parts):
                    continue
                
                # 檢查檔案類型
                if (file_path.suffix.lower() in self.config.target_extensions or 
                    file_path.name in self.config.target_extensions):
                    files.append(file_path)
            
        except Exception as e:
            self.logger.error(f"掃描目錄 {directory} 失敗: {e}")
        
        return files
    
    def batch_process(self, file_paths: List[Path], converter, preview_mode: bool = False) -> List[FileProcessResult]:
        """
        批量處理檔案
        
        Args:
            file_paths: 檔案路徑列表
            converter: 轉換器實例
            preview_mode: 預覽模式
        
        Returns:
            List[FileProcessResult]: 處理結果列表
        """
        results = []
        
        for file_path in file_paths:
            result = self.process_file(file_path, converter, preview_mode)
            results.append(result)
        
        return results

    def rename_files_if_needed(self, directory_path: str):
        """重命名包含簡體中文的檔案名稱"""
        try:
            for root, dirs, files in os.walk(directory_path):
                # 處理檔案重命名
                for filename in files:
                    old_path = os.path.join(root, filename)
                    new_filename = self.converter.convert_text(filename)
                    
                    if new_filename != filename:
                        new_path = os.path.join(root, new_filename)
                        # 確保新檔名不會衝突
                        counter = 1
                        while os.path.exists(new_path):
                            name, ext = os.path.splitext(new_filename)
                            new_path = os.path.join(root, f"{name}_{counter}{ext}")
                            counter += 1
                        
                        os.rename(old_path, new_path)
                        self.statistics.record_file_rename(filename, os.path.basename(new_path))
                        logging.info(f"📝 檔名轉換: {filename} → {os.path.basename(new_path)}")
                
                # 處理目錄重命名（從深層到淺層）
                for dirname in dirs:
                    old_dir_path = os.path.join(root, dirname)
                    new_dirname = self.converter.convert_text(dirname)
                    
                    if new_dirname != dirname:
                        new_dir_path = os.path.join(root, new_dirname)
                        if not os.path.exists(new_dir_path):
                            os.rename(old_dir_path, new_dir_path)
                            logging.info(f"📁 目錄轉換: {dirname} → {new_dirname}")
                        
        except Exception as e:
            logging.error(f"檔名轉換失敗: {str(e)}")
