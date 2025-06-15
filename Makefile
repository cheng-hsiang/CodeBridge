# CodeBridge - Makefile
# 簡化常見開發操作

PYTHON = python3
PIP = pip3
PROJECT_DIR = .
SRC_DIR = src
TESTS_DIR = tests
EXAMPLES_DIR = examples

# 顏色定義
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help install test clean run examples docs lint format check

# 預設目標
help:
	@echo "$(GREEN)CodeBridge - 可用命令:$(NC)"
	@echo ""
	@echo "  $(YELLOW)setup$(NC)       - 設置開發環境"
	@echo "  $(YELLOW)install$(NC)     - 安裝套件"
	@echo "  $(YELLOW)test$(NC)        - 執行測試"
	@echo "  $(YELLOW)run$(NC)         - 執行 CodeBridge (預覽模式)"
	@echo "  $(YELLOW)run-convert$(NC) - 執行實際轉換"
	@echo "  $(YELLOW)examples$(NC)    - 執行使用範例"
	@echo "  $(YELLOW)clean$(NC)       - 清理臨時檔案"
	@echo "  $(YELLOW)lint$(NC)        - 程式碼檢查"
	@echo "  $(YELLOW)format$(NC)      - 程式碼格式化"
	@echo "  $(YELLOW)docs$(NC)        - 生成文件"
	@echo "  $(YELLOW)package$(NC)     - 打包發布"
	@echo ""
	@echo "$(GREEN)範例:$(NC)"
	@echo "  make run PATH=./my-project"
	@echo "  make run-convert PATH=./my-project EXTENSIONS=.py,.js"
	@echo ""

# 設置開發環境
setup:
	@echo "$(GREEN)設置 CodeBridge 開發環境...$(NC)"
	@$(PYTHON) -m venv venv || true
	@echo "$(YELLOW)虛擬環境已創建，請執行:$(NC)"
	@echo "  source venv/bin/activate  # Linux/Mac"
	@echo "  venv\\Scripts\\activate     # Windows"

# 安裝套件
install:
	@echo "$(GREEN)安裝 CodeBridge...$(NC)"
	@$(PIP) install -e .

# 安裝開發依賴
install-dev:
	@echo "$(GREEN)安裝開發依賴...$(NC)"
	@$(PIP) install -e .[dev]

# 執行測試
test:
	@echo "$(GREEN)執行 CodeBridge 測試...$(NC)"
	@$(PYTHON) $(TESTS_DIR)/test_codebridge.py

# 執行測試（詳細模式）
test-verbose:
	@echo "$(GREEN)執行詳細測試...$(NC)"
	@$(PYTHON) -m unittest $(TESTS_DIR).test_codebridge -v

# 測試覆蓋率
coverage:
	@echo "$(GREEN)執行測試覆蓋率分析...$(NC)"
	@coverage run $(TESTS_DIR)/test_codebridge.py
	@coverage report -m
	@coverage html

# 執行 CodeBridge (預設預覽模式)
run:
	@echo "$(GREEN)執行 CodeBridge (預覽模式)...$(NC)"
	@$(PYTHON) codebridge.py --preview $(if $(PATH),--path $(PATH),) $(if $(EXTENSIONS),--extensions $(EXTENSIONS),) $(if $(CUSTOM),--custom $(CUSTOM),)

# 執行實際轉換
run-convert:
	@echo "$(RED)執行 CodeBridge (實際轉換模式)...$(NC)"
	@echo "$(YELLOW)警告: 這將實際修改檔案!$(NC)"
	@read -p "確定要繼續嗎? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@$(PYTHON) codebridge.py $(if $(PATH),--path $(PATH),) $(if $(EXTENSIONS),--extensions $(EXTENSIONS),) $(if $(CUSTOM),--custom $(CUSTOM),)

# 執行基本範例
examples:
	@echo "$(GREEN)執行基本使用範例...$(NC)"
	@$(PYTHON) $(EXAMPLES_DIR)/basic_usage.py

# 執行進階範例
examples-advanced:
	@echo "$(GREEN)執行進階使用範例...$(NC)"
	@$(PYTHON) $(EXAMPLES_DIR)/advanced_usage.py

# 清理臨時檔案
clean:
	@echo "$(GREEN)清理臨時檔案...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.backup" -delete
	@rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/
	@echo "$(GREEN)清理完成$(NC)"

# 程式碼檢查
lint:
	@echo "$(GREEN)執行程式碼檢查...$(NC)"
	@$(PYTHON) -m flake8 $(SRC_DIR) $(TESTS_DIR) --max-line-length=100 || echo "$(YELLOW)flake8 未安裝，跳過檢查$(NC)"

# 程式碼格式化
format:
	@echo "$(GREEN)格式化程式碼...$(NC)"
	@$(PYTHON) -m black $(SRC_DIR) $(TESTS_DIR) $(EXAMPLES_DIR) || echo "$(YELLOW)black 未安裝，跳過格式化$(NC)"

# 型別檢查
typecheck:
	@echo "$(GREEN)執行型別檢查...$(NC)"
	@$(PYTHON) -m mypy $(SRC_DIR) || echo "$(YELLOW)mypy 未安裝，跳過型別檢查$(NC)"

# 完整檢查
check: lint typecheck test
	@echo "$(GREEN)所有檢查完成$(NC)"

# 生成文件
docs:
	@echo "$(GREEN)生成文件...$(NC)"
	@echo "API 文件: docs/API.md"
	@echo "使用說明: README.md"

# 顯示統計資訊
stats:
	@echo "$(GREEN)CodeBridge 專案統計:$(NC)"
	@echo "程式碼行數:"
	@find $(SRC_DIR) -name "*.py" -exec wc -l {} + | tail -1
	@echo "測試檔案:"
	@find $(TESTS_DIR) -name "*.py" -exec wc -l {} + | tail -1
	@echo "總檔案數:"
	@find . -name "*.py" | wc -l

# 打包
package:
	@echo "$(GREEN)打包 CodeBridge...$(NC)"
	@$(PYTHON) setup.py sdist bdist_wheel
	@echo "$(GREEN)打包完成，檔案位於 dist/$(NC)"

# 測試安裝
test-install:
	@echo "$(GREEN)測試安裝...$(NC)"
	@$(PIP) install dist/*.whl --force-reinstall

# 發布到 PyPI (測試)
publish-test:
	@echo "$(GREEN)發布到 PyPI 測試環境...$(NC)"
	@twine upload --repository testpypi dist/* || echo "$(YELLOW)twine 未安裝$(NC)"

# 發布到 PyPI
publish:
	@echo "$(RED)發布到 PyPI...$(NC)"
	@echo "$(YELLOW)警告: 這將發布到正式 PyPI!$(NC)"
	@read -p "確定要繼續嗎? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@twine upload dist/* || echo "$(YELLOW)twine 未安裝$(NC)"

# 創建範例專案
create-demo:
	@echo "$(GREEN)創建演示專案...$(NC)"
	@mkdir -p demo/src demo/tests demo/docs
	@echo "# 这是一个简体中文演示文件\n数据处理和算法优化" > demo/src/main.py
	@echo "# 测试文件\n人工智能和机器学习" > demo/tests/test_main.py
	@echo "# 项目说明\n这是一个用于演示CodeBridge功能的项目" > demo/docs/README.md
	@echo "$(GREEN)演示專案已創建於 demo/ 目錄$(NC)"

# 演示轉換
demo: create-demo
	@echo "$(GREEN)演示 CodeBridge 轉換功能...$(NC)"
	@echo "$(YELLOW)轉換前:$(NC)"
	@cat demo/src/main.py
	@echo ""
	@echo "$(YELLOW)執行轉換...$(NC)"
	@$(PYTHON) codebridge.py --path demo --preview
	@echo ""
	@read -p "是否執行實際轉換? (y/N): " confirm && [ "$$confirm" = "y" ] && $(PYTHON) codebridge.py --path demo || echo "$(YELLOW)取消轉換$(NC)"

# 版本資訊
version:
	@echo "$(GREEN)CodeBridge 版本資訊:$(NC)"
	@grep "__version__" $(SRC_DIR)/__init__.py || echo "版本: 2.0.0"

# 顯示配置
config:
	@echo "$(GREEN)當前配置:$(NC)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "工作目錄: $(shell pwd)"
	@echo "專案目錄: $(PROJECT_DIR)"
	@echo "源碼目錄: $(SRC_DIR)"

# 快速開始
quickstart: setup install test examples
	@echo "$(GREEN)CodeBridge 快速開始完成!$(NC)"
	@echo "$(YELLOW)現在可以執行:$(NC)"
	@echo "  make run PATH=你的專案路徑"

# 開發模式
dev: install-dev lint format test
	@echo "$(GREEN)開發環境準備完成$(NC)"
