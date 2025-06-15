# 🌉 CodeBridge - 程式碼簡繁轉換工具

vibe coding 到一半 還不知道效果如何 見諒

> **Advanced Simplified to Traditional Chinese Converter for Development Projects**
> 
> 專為軟體開發專案設計的智慧型簡體轉繁體中文工具

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](https://github.com/codebridge)

## ✨ 特色功能

- 🎯 **專為開發專案優化** - 深度理解程式碼結構和技術術語
- 📚 **4000+ 專業術語字庫** - 涵蓋 AI、雲端、區塊鏈、IoT 等現代技術
- 🔍 **智慧預覽模式** - 安全查看轉換結果，避免意外修改
- ⚙️ **自定義映射支援** - 輕鬆添加專案特定術語
- 🚀 **智慧檔案識別** - 自動處理 20+ 種開發檔案類型
- 📊 **詳細統計報告** - 完整的轉換分析和效能指標
- 🛡️ **安全可靠** - 支援備份、錯誤恢復、編碼檢測

## 🚀 快速開始

### 安裝需求

- Python 3.6 或更高版本
- 支援 Windows、macOS、Linux

### 基本使用

```bash
# 基本轉換（預設處理當前目錄）
python codebridge.py

# 指定專案路徑
python codebridge.py --path /path/to/your/project

# 預覽模式（安全查看轉換結果）
python codebridge.py --preview

# 使用自定義映射
python codebridge.py --custom custom_mappings.txt

# 指定檔案類型
python codebridge.py --extensions .py,.js,.vue,.md
```

### 進階用法

```bash
# 組合使用多個選項
python codebridge.py \
    --path ./my-project \
    --preview \
    --custom company_terms.txt \
    --extensions .py,.js,.ts,.vue,.md,.json \
    --output report.md

# 使用配置檔案
python codebridge.py --config config/advanced.json

# 查看版本資訊
python codebridge.py --version
```

## 📁 專案結構

```
transcoder/
├── src/                     # 核心源碼
│   ├── __init__.py         # 套件初始化
│   ├── codebridge.py       # 主要轉換工具
│   ├── converter.py        # 中文轉換器
│   ├── mappings.py         # 映射管理器
│   ├── file_processor.py   # 檔案處理器
│   ├── config.py          # 配置管理
│   └── statistics.py      # 統計收集器
├── tests/                  # 測試檔案
│   ├── __init__.py
│   └── test_codebridge.py
├── examples/               # 使用範例
│   ├── basic_usage.py      # 基本使用範例
│   └── advanced_usage.py   # 進階使用範例
├── config/                 # 配置檔案
│   └── default.json        # 預設配置
├── data/                   # 資料檔案
│   └── custom_mappings_example.txt
├── docs/                   # 文件目錄
├── codebridge.py          # 主執行檔案
├── requirements.txt       # 相依套件
├── setup.py              # 安裝腳本
└── README.md             # 專案說明
```

## 🎯 支援的檔案類型

### 程式語言
`.py` `.js` `.jsx` `.ts` `.tsx` `.vue` `.java` `.c` `.cpp` `.cs` `.go` `.rs` `.php` `.rb` `.swift` `.kt` `.scala`

### 設定與資料
`.json` `.yaml` `.yml` `.xml` `.toml` `.ini` `.conf` `.config` `.env` `.properties`

### 文件與腳本
`.md` `.txt` `.rst` `.html` `.htm` `.css` `.scss` `.sass` `.less` `.sh` `.bat` `.ps1`

### 建置工具
`.dockerfile` `.makefile` `.cmake` `.gradle` `.maven` `.npm` `.lock` `.gitignore`

## 📚 字庫涵蓋範圍

### 🏗️ 基礎開發 (1,200+ 詞彙)
- **程式語言術語**: 變數、函數、類別、物件、方法
- **軟體工程**: 需求分析、設計模式、測試驅動開發
- **版本控制**: 分支管理、合併請求、程式碼審查
- **開發流程**: 敏捷開發、持續整合、自動化部署

### 🚀 現代技術 (1,800+ 詞彙)
- **人工智慧/機器學習**: 深度學習、神經網路、自然語言處理、特徵工程
- **雲端原生**: 容器化、微服務、服務網格、無伺服器架構
- **區塊鏈/Web3**: 智慧合約、去中心化、加密貨幣、共識機制
- **物聯網/邊緣**: 感測器網路、邊緣運算、設備管理、遠端控制
- **量子計算**: 量子演算法、量子程式設計、量子機器學習

### 💼 商業管理 (600+ 詞彙)
- **專案管理**: 敏捷開發、看板方法、使用者故事、里程碑
- **產品開發**: 需求分析、使用者體驗、原型設計、迭代開發
- **團隊協作**: 程式碼審查、技術分享、知識管理、最佳實務

### 🔒 安全與合規 (800+ 詞彙)
- **資訊安全**: 認證授權、權限控制、威脅建模、漏洞掃描
- **DevSecOps**: 安全左移、安全開發、滲透測試、安全稽核
- **合規管理**: 風險評估、合規檢查、資料隱私、安全治理

## 🔧 使用範例

### 基本轉換

```python
from src.codebridge import CodeBridge

# 初始化
codebridge = CodeBridge()

# 轉換專案
result = codebridge.convert_project("/path/to/project")

print(f"處理檔案: {result.processed_files}")
print(f"轉換字符: {result.total_conversions}")
```

### 自定義映射

```python
# 載入自定義映射檔案
codebridge.load_custom_mappings("company_terms.txt")

# 動態添加映射
codebridge.mapping_manager.add_custom_mapping("我们的API", "我們的API")
```

### 配置管理

```python
from src.config import Config

# 創建自定義配置
config = Config()
config.add_target_extension("log")
config.set_config("create_backup", True)

# 使用配置
codebridge = CodeBridge(config)
```

## 📊 範例輸出

```
🌉 CodeBridge - 程式碼簡繁轉換工具
======================================================================
執行模式: 轉換模式
專案路徑: /path/to/my-project
處理檔案類型: .py,.js,.ts,.vue,.md
總字庫規模: 4,247 個映射

📊 字庫分類統計:
  • 基本字符: 1,205 個
  • 科技開發: 1,845 個  
  • 業務管理: 542 個
  • 系統架構: 655 個
  • 專業術語: 1,000 個
======================================================================

📊 處理結果:
掃描檔案總數: 156
實際處理檔案數量: 23
實際轉換字符總數: 2,341

🔄 已轉換詳情 (前10個檔案):
  • main.py: 145 個字符
  • api.js: 89 個字符
  • README.md: 234 個字符
  • config.json: 45 個字符

✅ 沒有錯誤
======================================================================
🎉 轉換完成！
📈 平均每個檔案轉換: 101.8 個字符
💡 建議：定期執行此腳本以保持程式碼的繁體中文一致性

🌉 CodeBridge - Bridging the gap between Simplified and Traditional Chinese in code!
```

## 🛠️ 自定義映射格式

創建 `custom_mappings.txt` 檔案：

```
# 公司特定術語
我们公司:我們公司
内部系统:內部系統
业务逻辑:業務邏輯

# API 相關
接口文档:介面文件
请求参数:請求參數
响应数据:回應資料

# 功能模組
登录模块:登入模組
支付模块:支付模組
搜索模块:搜尋模組
```

## ⚙️ 配置選項

### 主要配置項目

| 選項 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `target_extensions` | List | 20+ 類型 | 要處理的檔案類型 |
| `exclude_dirs` | List | 常見排除目錄 | 要排除的目錄 |
| `max_file_size` | Int | 10MB | 最大檔案大小限制 |
| `create_backup` | Bool | false | 是否創建備份檔案 |
| `log_level` | String | "INFO" | 日誌級別 |
| `parallel_processing` | Bool | false | 是否啟用平行處理 |

### 設定範例

```json
{
  "target_extensions": [".py", ".js", ".md"],
  "exclude_dirs": ["node_modules", "venv", ".git"],
  "max_file_size": 5242880,
  "create_backup": true,
  "log_level": "DEBUG"
}
```

## 🧪 測試

```bash
# 執行所有測試
python tests/test_codebridge.py

# 執行特定測試
python -m unittest tests.test_codebridge.TestChineseConverter

# 執行範例
python examples/basic_usage.py
python examples/advanced_usage.py
```

### 開發設定

```bash
# 複製專案
git clone https://github.com/your-username/codebridge.git
cd codebridge

# 設定虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 安裝開發相依套件
pip install -r requirements.txt

# 執行測試
python tests/test_codebridge.py
```

## 📄 授權

本專案採用 [MIT License](LICENSE) 授權 - 查看 LICENSE 檔案了解詳情。

## 🙋‍♂️ 常見問題

### Q: 如何處理特殊編碼的檔案？
A: CodeBridge 支援自動編碼檢測，可處理 UTF-8、GBK、Big5 等常見編碼。

### Q: 可以批量處理多個專案嗎？
A: 可以，參考 `examples/advanced_usage.py` 中的批量處理範例。

### Q: 如何確保轉換的準確性？
A: 建議先使用 `--preview` 模式查看轉換結果，確認無誤後再執行實際轉換。

### Q: 支援哪些作業系統？
A: 支援 Windows、macOS、Linux 等所有支援 Python 3.6+ 的系統。

### Q: 如何報告問題或建議新功能？
A: 請在 GitHub Issues 中提出，我們會盡快回應。

---

**CodeBridge** - *Bridging the gap between Simplified and Traditional Chinese in code* 🌉

*讓程式碼中的中文轉換變得簡單而智慧！*
