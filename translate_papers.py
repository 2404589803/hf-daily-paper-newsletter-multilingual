import os
import json
import time
import logging
import sys
import argparse
import openai
from utils import setup_logger
from datetime import datetime

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
            api_key: InternLM API密钥 (JWT 格式)
        """
        try:
            if not api_key or api_key == "your_api_key_here":
                raise ValueError("请提供有效的 InternLM API 密钥")
                
            # 使用 0.28.1 版本的配置方式
            openai.api_key = api_key
            openai.api_base = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"
            # 添加 JWT 认证头
            openai.api_type = "open_ai"
            openai.default_headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            self.max_retries = 3
            self.retry_delay = 3
            self.request_delay = 1
            logger.info("成功初始化 InternLM API 客户端")
        except ValueError as ve:
            logger.error(f"API 密钥错误: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"初始化 InternLM API 客户端时发生错误: {str(e)}")
            raise
        
    def translate_paper(self, paper_data, target_lang, paper_index=None, total_papers=None):
        """
        翻译单篇论文数据
        Args:
            paper_data: 论文数据字典
            target_lang: 目标语言代码
            paper_index: 当前论文索引（用于显示进度）
            total_papers: 总论文数（用于显示进度）
        Returns:
            dict: 翻译后的论文数据
        """
        try:
            if not paper_data or 'paper' not in paper_data:
                raise ValueError("无效的论文数据格式")
                
            translated_paper = paper_data.copy()
            paper_info = translated_paper['paper']
            
            # 检查必要字段
            required_fields = ['title', 'summary']
            for field in required_fields:
                if field not in paper_info:
                    raise ValueError(f"论文数据缺少必要字段: {field}")
                if not paper_info[field]:
                    raise ValueError(f"论文{field}字段为空")
            
            # 显示进度
            progress_info = ""
            if paper_index is not None and total_papers is not None:
                progress_info = f"[{paper_index}/{total_papers}] "
            
            # 翻译标题
            logger.info(f"{progress_info}正在翻译论文标题: {paper_info['title'][:50]}...")
            translated_title = self._translate_text(paper_info['title'], target_lang)
            if not translated_title:
                raise ValueError("标题翻译失败")
            paper_info['title'] = translated_title
            
            # 翻译摘要
            logger.info(f"{progress_info}正在翻译论文摘要...")
            translated_summary = self._translate_text(paper_info['summary'], target_lang)
            if not translated_summary:
                raise ValueError("摘要翻译失败")
            paper_info['summary'] = translated_summary
            
            logger.info(f"{progress_info}论文翻译完成")
            return translated_paper
            
        except ValueError as ve:
            logger.error(f"{progress_info}论文数据处理错误: {str(ve)}")
            return None
        except Exception as e:
            logger.error(f"{progress_info}处理论文翻译时发生错误: {str(e)}")
            return None
            
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
            if not text or not text.strip():
                raise ValueError("待翻译文本为空")
                
            # 添加请求延迟
            if retry_count > 0:
                time.sleep(self.retry_delay)
            else:
                time.sleep(self.request_delay)
                
            prompt = f"""请将以下英文文本翻译成{SUPPORTED_LANGUAGES[target_lang]}，保持专业性和准确性：

{text}

只需返回翻译结果，不要添加任何解释或额外的文本。"""
            
            logger.info(f"正在将文本翻译成 {SUPPORTED_LANGUAGES[target_lang]}")
            
            # 使用 0.28.1 版本的 API 调用方式
            response = openai.ChatCompletion.create(
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
            
        except openai.error.AuthenticationError as ae:
            logger.error(f"API 认证失败: {str(ae)}")
            if retry_count < self.max_retries:
                retry_count += 1
                logger.info(f"正在进行第 {retry_count} 次重试...")
                return self._translate_text(text, target_lang, retry_count)
            raise
        except openai.error.APIError as api_err:
            logger.error(f"API 调用错误: {str(api_err)}")
            if retry_count < self.max_retries:
                retry_count += 1
                logger.info(f"正在进行第 {retry_count} 次重试...")
                return self._translate_text(text, target_lang, retry_count)
            return None
        except Exception as e:
            logger.error(f"翻译过程中发生错误: {str(e)}")
            if retry_count < self.max_retries:
                retry_count += 1
                logger.info(f"正在进行第 {retry_count} 次重试...")
                return self._translate_text(text, target_lang, retry_count)
            return None

def process_papers(api_key, date_str):
    """
    处理指定日期的论文数据并翻译成多种语言
    Args:
        api_key: InternLM API密钥
        date_str: 日期字符串 (YYYY-MM-DD)
    Returns:
        bool: 处理是否成功
    """
    try:
        # 验证日期格式
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            logger.error(f"无效的日期格式: {date_str}，应为 YYYY-MM-DD")
            return False
            
        # 读取原始论文数据
        input_file = os.path.join('Paper_metadata_download', f"{date_str}.json")
        if not os.path.exists(input_file):
            logger.error(f"找不到{date_str}的论文数据文件: {input_file}")
            return False
            
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                papers = json.load(f)
        except json.JSONDecodeError as je:
            logger.error(f"论文数据文件格式错误: {str(je)}")
            return False
        except Exception as e:
            logger.error(f"读取论文数据文件时发生错误: {str(e)}")
            return False
            
        if not papers:
            logger.error("论文数据为空")
            return False
            
        logger.info(f"成功读取 {len(papers)} 篇论文数据")
        
        try:
            translator = PaperTranslator(api_key)
        except Exception as e:
            logger.error(f"初始化翻译器失败: {str(e)}")
            return False
        
        # 为每种语言创建输出目录
        total_languages = len(SUPPORTED_LANGUAGES)
        success_count = 0
        
        for lang_index, (lang_code, lang_name) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
            try:
                logger.info(f"[{lang_index}/{total_languages}] 开始处理 {lang_name} 翻译...")
                
                output_dir = os.path.join('Translated_papers', lang_code)
                os.makedirs(output_dir, exist_ok=True)
                
                # 翻译并保存论文
                translated_papers = []
                for i, paper in enumerate(papers, 1):
                    try:
                        translated_paper = translator.translate_paper(paper, lang_code, i, len(papers))
                        if translated_paper:
                            translated_papers.append(translated_paper)
                        else:
                            logger.warning(f"[{lang_index}/{total_languages}] 第 {i} 篇论文翻译失败")
                    except Exception as e:
                        logger.error(f"[{lang_index}/{total_languages}] 翻译第 {i} 篇论文时发生错误: {str(e)}")
                        continue
                    
                # 保存翻译后的数据
                if translated_papers:
                    output_file = os.path.join(output_dir, f"{date_str}.json")
                    try:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(translated_papers, f, ensure_ascii=False, indent=2)
                        logger.info(f"[{lang_index}/{total_languages}] 已将 {len(translated_papers)} 篇论文翻译成 {lang_name} 并保存")
                        success_count += 1
                    except Exception as e:
                        logger.error(f"[{lang_index}/{total_languages}] 保存翻译结果时发生错误: {str(e)}")
                else:
                    logger.error(f"[{lang_index}/{total_languages}] 没有论文被成功翻译成 {lang_name}")
            except Exception as e:
                logger.error(f"[{lang_index}/{total_languages}] 处理 {lang_name} 翻译时发生错误: {str(e)}")
                continue
        
        # 如果至少有一种语言翻译成功，就认为整体处理成功
        if success_count > 0:
            logger.info(f"翻译处理完成，共 {total_languages} 种语言，成功 {success_count} 种")
            return True
        else:
            logger.error("所有语言的翻译都失败了")
            return False
        
    except Exception as e:
        logger.error(f"处理论文数据时发生错误: {str(e)}")
        return False

def process_papers_in_range(api_key, start_date_str, end_date_str):
    """
    处理指定日期范围内的论文数据并翻译成多种语言
    Args:
        api_key: InternLM API密钥
        start_date_str: 开始日期，格式为YYYY-MM-DD
        end_date_str: 结束日期，格式为YYYY-MM-DD
    Returns:
        bool: 处理是否成功
    """
    try:
        # 验证日期格式
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if start_date > end_date:
                logger.error("开始日期不能晚于结束日期")
                return False
        except ValueError as e:
            logger.error(f"日期格式错误: {str(e)}")
            return False

        success_count = 0
        total_days = (end_date - start_date).days + 1
        current_date = start_date

        while current_date <= end_date:
            current_date_str = current_date.strftime('%Y-%m-%d')
            logger.info(f"正在处理日期: {current_date_str}")
            
            if process_papers(api_key, current_date_str):
                success_count += 1
            
            current_date += datetime.timedelta(days=1)

        # 如果至少有一天处理成功，就认为整体处理成功
        if success_count > 0:
            logger.info(f"日期范围处理完成，共 {total_days} 天，成功 {success_count} 天")
            return True
        else:
            logger.error("所有日期的处理都失败了")
            return False

    except Exception as e:
        logger.error(f"处理日期范围内的论文数据时发生错误: {str(e)}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='翻译论文数据')
    parser.add_argument('--date', type=str, help='论文日期 (YYYY-MM-DD)')
    parser.add_argument('--start_date', type=str, help='翻译范围的开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='翻译范围的结束日期 (YYYY-MM-DD)')
    parser.add_argument('--api_key', required=True, help='InternLM API密钥')
    
    args = parser.parse_args()
    
    # 处理日期范围翻译
    if args.start_date and args.end_date:
        if args.date:
            logger.warning("同时指定了单个日期和日期范围，将优先处理日期范围")
        if process_papers_in_range(args.api_key, args.start_date, args.end_date):
            logger.info("日期范围内的论文翻译处理完成")
            return 0
        else:
            logger.error("日期范围内的论文翻译处理失败")
            return 1
    else:
        # 处理单个日期
        if process_papers(args.api_key, args.date):
            logger.info("论文翻译处理完成")
            return 0
        else:
            logger.error("论文翻译处理失败")
            return 1

if __name__ == "__main__":
    sys.exit(main())