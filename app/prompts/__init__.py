# app/prompts/__init__.py
import os
from functools import lru_cache

import yaml

from app.core.config import ROOT_DIR


class PromptManager:
    def __init__(self):
        self.prompt_dir = os.path.join(ROOT_DIR, "app", "prompts")

    @lru_cache(maxsize=128)
    def load_prompt(self, relative_path: str) -> dict:
        """
        读取 YAML 提示词文件并返回字典
        :param relative_path: 如 'chat/general.yaml'
        """
        file_path = os.path.join(self.prompt_dir, relative_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            # 使用 safe_load 防止安全隐患
            return yaml.safe_load(f)

    def get_system_prompt(self, relative_path: str) -> str:
        """快速获取系统提示词内容"""
        data = self.load_prompt(relative_path)
        return data.get("messages", {}).get("system", "")


prompt_manager = PromptManager()
