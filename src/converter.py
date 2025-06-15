#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 中文轉換器核心模組
"""

from typing import Dict, List, Tuple, Set
import re


class ChineseConverter:
    """
    中文轉換器類
    
    負責執行實際的簡體轉繁體轉換
    """
    
    def __init__(self, mapping_manager):
        """
        初始化轉換器
        
        Args:
            mapping_manager: 映射管理器實例
        """
        self.mapping_manager = mapping_manager
        self._sorted_mappings = None
        self._update_sorted_mappings()
    
    def _update_sorted_mappings(self):
        """更新已排序的映射（按長度降序）"""
        all_mappings = self.mapping_manager.get_all_mappings()
        self._sorted_mappings = sorted(
            all_mappings.items(), 
            key=lambda x: len(x[0]), 
            reverse=True
        )
    
    def convert_text(self, text: str) -> Tuple[str, int]:
        """
        轉換文本中的簡體中文為繁體中文
        
        Args:
            text: 要轉換的文本
        
        Returns:
            Tuple[str, int]: (轉換後的文本, 轉換次數)
        """
        if not text:
            return text, 0
        
        # 如果映射已更新，重新排序
        if self.mapping_manager.is_mappings_updated():
            self._update_sorted_mappings()
        
        converted = text
        total_count = 0
        
        # 按照詞彙長度排序，優先轉換長詞彙
        for simplified, traditional in self._sorted_mappings:
            if simplified in converted and simplified != traditional:
                count = converted.count(simplified)
                if count > 0:
                    converted = converted.replace(simplified, traditional)
                    total_count += count
        
        return converted, total_count
    
    def preview_conversion(self, text: str) -> List[Tuple[str, str, int]]:
        """
        預覽轉換結果，不實際修改文本
        
        Args:
            text: 要分析的文本
        
        Returns:
            List[Tuple[str, str, int]]: [(簡體詞, 繁體詞, 出現次數), ...]
        """
        if not text:
            return []
        
        conversions = []
        
        for simplified, traditional in self._sorted_mappings:
            if simplified in text and simplified != traditional:
                count = text.count(simplified)
                if count > 0:
                    conversions.append((simplified, traditional, count))
        
        return conversions
    
    def find_chinese_text(self, text: str) -> List[Tuple[int, int, str]]:
        """
        找出文本中的中文內容
        
        Args:
            text: 要分析的文本
        
        Returns:
            List[Tuple[int, int, str]]: [(開始位置, 結束位置, 中文內容), ...]
        """
        chinese_pattern = r'[\u4e00-\u9fff]+'
        matches = []
        
        for match in re.finditer(chinese_pattern, text):
            start, end = match.span()
            chinese_text = match.group()
            matches.append((start, end, chinese_text))
        
        return matches
    
    def validate_mapping(self, simplified: str, traditional: str) -> bool:
        """
        驗證映射的有效性
        
        Args:
            simplified: 簡體詞
            traditional: 繁體詞
        
        Returns:
            bool: 映射是否有效
        """
        # 基本檢查
        if not simplified or not traditional:
            return False
        
        # 檢查是否包含中文
        chinese_pattern = r'[\u4e00-\u9fff]'
        if not re.search(chinese_pattern, simplified) or not re.search(chinese_pattern, traditional):
            return False
        
        # 檢查長度合理性
        if len(simplified) > 50 or len(traditional) > 50:
            return False
        
        return True
    
    def get_conversion_statistics(self, text: str) -> Dict[str, int]:
        """
        獲取文本的轉換統計信息
        
        Args:
            text: 要分析的文本
        
        Returns:
            Dict[str, int]: 統計信息
        """
        stats = {
            'total_chars': len(text),
            'chinese_chars': 0,
            'convertible_chars': 0,
            'conversion_mappings': 0
        }
        
        # 計算中文字符數
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        stats['chinese_chars'] = len(chinese_chars)
        
        # 計算可轉換的字符數和映射數
        conversions = self.preview_conversion(text)
        stats['conversion_mappings'] = len(conversions)
        stats['convertible_chars'] = sum(len(simplified) * count for simplified, _, count in conversions)
        
        return stats
    
    def batch_convert(self, texts: List[str]) -> List[Tuple[str, int]]:
        """
        批量轉換多個文本
        
        Args:
            texts: 文本列表
        
        Returns:
            List[Tuple[str, int]]: [(轉換後的文本, 轉換次數), ...]
        """
        results = []
        for text in texts:
            converted, count = self.convert_text(text)
            results.append((converted, count))
        return results
    
    def get_unique_conversions(self, text: str) -> Set[Tuple[str, str]]:
        """
        獲取文本中的唯一轉換對
        
        Args:
            text: 要分析的文本
        
        Returns:
            Set[Tuple[str, str]]: 唯一的(簡體, 繁體)對
        """
        conversions = self.preview_conversion(text)
        return set((simplified, traditional) for simplified, traditional, _ in conversions)
