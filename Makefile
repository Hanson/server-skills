SKILLS := server-list server-add server-del server-check server-ssh
HOME_UNIX := $(shell echo ~)
SKILLS_DIR := $(HOME_UNIX)/.claude/skills
DATA_DIR := $(HOME_UNIX)/.claude/servers

.PHONY: install uninstall list clean

# 安装所有插件
install:
	@mkdir -p $(SKILLS_DIR)
	@for skill in $(SKILLS); do \
		cp -r $$skill $(SKILLS_DIR)/; \
		echo "Installed: $$skill"; \
	done
	@mkdir -p $(DATA_DIR)
	@if [ ! -f $(DATA_DIR)/servers.json ]; then \
		echo '{"servers":[]}' > $(DATA_DIR)/servers.json; \
		echo "Created: $(DATA_DIR)/servers.json"; \
	fi
	@echo "\nDone! All plugins installed to $(SKILLS_DIR)"

# 卸载所有插件
uninstall:
	@for skill in $(SKILLS); do \
		rm -rf $(SKILLS_DIR)/$$skill; \
		echo "Removed: $$skill"; \
	done
	@echo "\nDone! All plugins removed."

# 删除服务器数据（慎用）
clean: uninstall
	@rm -rf $(DATA_DIR)
	@echo "Removed: $(DATA_DIR)"

# 查看已安装状态
list:
	@echo "Plugin install status:\n"
	@for skill in $(SKILLS); do \
		if [ -d $(SKILLS_DIR)/$$skill ]; then \
			echo "  [x] $$skill"; \
		else \
			echo "  [ ] $$skill"; \
		fi; \
	done
	@echo ""
	@if [ -f $(DATA_DIR)/servers.json ]; then \
		servers=$$(grep -c '"name"' $(DATA_DIR)/servers.json 2>/dev/null || echo "?"); \
		echo "Servers registered: $$servers"; \
	else \
		echo "Servers registered: 0 (no data file)"; \
	fi
