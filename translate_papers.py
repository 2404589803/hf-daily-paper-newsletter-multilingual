import os
import json
import time
import logging
from openai import OpenAI
from utils import setup_logger

# 设置日志记录器
logger = setup_logger()

# 支持的语言列表（只保留需要翻译的语言）
SUPPORTED_LANGUAGES = {
    'ja': '日本語',
    'ko': '한국어',
    'es': 'Español',
    'fr': 'Français',
}

class PaperTranslator:
    def __init__(self, api_key):
        """
        初始化翻译器
        Args:
            api_key: InternLM API密钥
        """
        try:
            # 初始化客户端，使用最简单的配置
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://internlm-chat.intern-ai.org.cn/puyu/api/v1"
            )
            self.max_retries = 5
            self.retry_delay = 5
            self.request_delay = 3
            logger.info("成功初始化 InternLM API 客户端")
        except Exception as e:
            logger.error(f"初始化 InternLM API 客户端时发生错误: {str(e)}")
            raise
        
    def _translate_text(self, text, target_lang, retry_count=0):
        """
        使用InternLM翻译文本，包含重试机制
        Args:
            text: 要翻译的文本
            target_lang: 目标语言
            retry_count: 当前重试次数
        Returns:
            str: 翻译后的文本
        """
        try:
            # 添加请求延迟
            if retry_count > 0:
                time.sleep(self.retry_delay)
            else:
                time.sleep(self.request_delay)
                
            prompt = f"""请将以下英文文本翻译成{SUPPORTED_LANGUAGES[target_lang]}，保持专业性和准确性：

{text}

只需返回翻译结果，不要添加任何解释或额外的文本。"""
            
            logger.info(f"正在将文本翻译成 {SUPPORTED_LANGUAGES[target_lang]}")
            
            # 根据官方文档设置参数
            response = self.client.chat.completions.create(
                model="internlm3-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                top_p=0.9,
                n=1
            )
            
            translated_text = response.choices[0].message.content.strip()
            if not translated_text:
                raise ValueError("翻译结果为空")
                
            return translated_text
            
        except Exception as e:
            logger.error(f"翻译过程中发生错误: {str(e)}")
            
            # 如果还有重试机会，则重试
            if retry_count < self.max_retries:
                retry_count += 1
                logger.info(f"正在进行第 {retry_count} 次重试...")
                return self._translate_text(text, target_lang, retry_count)
            
            return None

    def translate_paper(self, paper_data, target_lang):
        """
        翻译单篇论文数据
        Args:
            paper_data: 论文数据字典
            target_lang: 目标语言代码
        Returns:
            dict: 翻译后的论文数据
        """
        try:
            translated_paper = paper_data.copy()
            paper_info = translated_paper['paper']
            
            # 翻译标题
            logger.info(f"正在翻译论文标题: {paper_info['title'][:50]}...")
            translated_title = self._translate_text(paper_info['title'], target_lang)
            if not translated_title:
                raise ValueError("标题翻译失败")
            paper_info['title'] = translated_title
            
            # 翻译摘要
            logger.info("正在翻译论文摘要...")
            translated_summary = self._translate_text(paper_info['summary'], target_lang)
            if not translated_summary:
                raise ValueError("摘要翻译失败")
            paper_info['summary'] = translated_summary
            
            return translated_paper
            
        except Exception as e:
            logger.error(f"处理论文翻译时发生错误: {str(e)}")
            return None

def process_papers(api_key, date_str):
    """
    处理指定日期的论文数据并翻译成多种语言
    Args:
        api_key: InternLM API密钥
        date_str: 日期字符串 (YYYY-MM-DD)
    """
    try:
        # 读取原始论文数据
        input_file = os.path.join('Paper_metadata_download', f"{date_str}.json")
        if not os.path.exists(input_file):
            logger.error(f"找不到{date_str}的论文数据文件")
            return False
            
        with open(input_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
            
        logger.info(f"成功读取 {len(papers)} 篇论文数据")
        translator = PaperTranslator(api_key)
        
        # 为每种语言创建输出目录
        for lang_code in SUPPORTED_LANGUAGES.keys():
            output_dir = os.path.join('Translated_papers', lang_code)
            os.makedirs(output_dir, exist_ok=True)
            
            logger.info(f"开始翻译成 {SUPPORTED_LANGUAGES[lang_code]}...")
            
            # 翻译并保存论文
            translated_papers = []
            for i, paper in enumerate(papers, 1):
                logger.info(f"正在翻译第 {i}/{len(papers)} 篇论文...")
                translated_paper = translator.translate_paper(paper, lang_code)
                if translated_paper:
                    translated_papers.append(translated_paper)
                    
            # 保存翻译后的数据
            if translated_papers:
                output_file = os.path.join(output_dir, f"{date_str}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(translated_papers, f, ensure_ascii=False, indent=2)
                    
                logger.info(f"已将 {len(translated_papers)} 篇论文翻译成 {SUPPORTED_LANGUAGES[lang_code]} 并保存")
            else:
                logger.error(f"没有论文被成功翻译成 {SUPPORTED_LANGUAGES[lang_code]}")
            
        return True
        
    except Exception as e:
        logger.error(f"处理论文数据时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    # 获取命令行参数
    date = sys.argv[2]  # --date 后面的值
    api_key = sys.argv[4]  # --api_key 后面的值
    
    if process_papers(api_key, date):
        logger.info("论文翻译处理完成")
        exit(0)
    else:
        logger.error("论文翻译处理失败")
        exit(1) 