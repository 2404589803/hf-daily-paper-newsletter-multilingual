import os
import json
import logging
import argparse
import sys
from datetime import datetime
from gtts import gTTS
from utils import setup_logger

# 设置日志记录器
logger = setup_logger()

# 支持的语言列表（与翻译语言对应）
SUPPORTED_LANGUAGES = {
    'ja': {'code': 'ja', 'name': '日本語', 'tts_code': 'ja'},
    'ko': {'code': 'ko', 'name': '한국어', 'tts_code': 'ko'},
    'es': {'code': 'es', 'name': 'Español', 'tts_code': 'es'},
    'fr': {'code': 'fr', 'name': 'Français', 'tts_code': 'fr'},
}

def generate_audio_for_paper(paper_data, lang_code):
    """
    为单篇论文生成语音文件
    Args:
        paper_data: 论文数据字典
        lang_code: 语言代码
    Returns:
        tuple: (是否成功, 生成的音频文件路径)
    """
    try:
        if not paper_data or 'paper' not in paper_data:
            raise ValueError("无效的论文数据格式")
            
        paper_info = paper_data['paper']
        
        # 检查必要字段
        required_fields = ['title', 'summary', 'id']
        for field in required_fields:
            if field not in paper_info:
                raise ValueError(f"论文数据缺少必要字段: {field}")
            if not paper_info[field]:
                raise ValueError(f"论文{field}字段为空")
        
        # 准备要转换为语音的文本
        text_to_speak = f"{paper_info['title']}。{paper_info['summary']}"
        
        # 创建语音文件的目录
        output_dir = os.path.join('Audio_papers', lang_code)
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成音频文件名（使用论文ID）
        audio_filename = f"{paper_info['id']}.mp3"
        audio_path = os.path.join(output_dir, audio_filename)
        
        # 生成语音
        tts = gTTS(text=text_to_speak, lang=SUPPORTED_LANGUAGES[lang_code]['tts_code'], slow=False)
        tts.save(audio_path)
        
        logger.info(f"成功生成论文 {paper_info['id']} 的{SUPPORTED_LANGUAGES[lang_code]['name']}语音文件")
        return True, audio_path
        
    except Exception as e:
        logger.error(f"生成论文语音时发生错误: {str(e)}")
        return False, None

def process_papers(date_str):
    """
    处理指定日期的论文数据并生成语音文件
    Args:
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
        
        success_count = 0
        total_languages = len(SUPPORTED_LANGUAGES)
        
        # 为每种语言处理翻译后的论文
        for lang_index, (lang_code, lang_info) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
            try:
                # 读取翻译后的论文数据
                input_file = os.path.join('Translated_papers', lang_code, f"{date_str}.json")
                if not os.path.exists(input_file):
                    logger.warning(f"找不到{date_str}的{lang_info['name']}翻译文件: {input_file}")
                    continue
                
                with open(input_file, 'r', encoding='utf-8') as f:
                    papers = json.load(f)
                
                if not papers:
                    logger.warning(f"{date_str}的{lang_info['name']}翻译数据为空")
                    continue
                
                logger.info(f"[{lang_index}/{total_languages}] 开始为 {lang_info['name']} 生成语音...")
                
                # 为每篇论文生成语音
                success_papers = 0
                for i, paper in enumerate(papers, 1):
                    success, audio_path = generate_audio_for_paper(paper, lang_code)
                    if success:
                        success_papers += 1
                
                if success_papers > 0:
                    logger.info(f"[{lang_index}/{total_languages}] 成功生成 {success_papers}/{len(papers)} 篇论文的{lang_info['name']}语音")
                    success_count += 1
                
            except Exception as e:
                logger.error(f"[{lang_index}/{total_languages}] 处理{lang_info['name']}语音时发生错误: {str(e)}")
                continue
        
        # 如果至少有一种语言处理成功，就认为整体处理成功
        if success_count > 0:
            logger.info(f"语音生成完成，共 {total_languages} 种语言，成功 {success_count} 种")
            return True
        else:
            logger.error("所有语言的语音生成都失败了")
            return False
            
    except Exception as e:
        logger.error(f"处理论文语音数据时发生错误: {str(e)}")
        return False

def process_papers_in_range(start_date_str, end_date_str):
    """
    处理指定日期范围内的论文数据并生成语音文件
    Args:
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
            
            if process_papers(current_date_str):
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
        logger.error(f"处理日期范围内的论文语音数据时发生错误: {str(e)}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成论文语音数据')
    parser.add_argument('--date', type=str, help='论文日期 (YYYY-MM-DD)')
    parser.add_argument('--start_date', type=str, help='生成范围的开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='生成范围的结束日期 (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # 处理日期范围生成
    if args.start_date and args.end_date:
        if args.date:
            logger.warning("同时指定了单个日期和日期范围，将优先处理日期范围")
        if process_papers_in_range(args.start_date, args.end_date):
            logger.info("日期范围内的论文语音生成完成")
            return 0
        else:
            logger.error("日期范围内的论文语音生成失败")
            return 1
    else:
        # 处理单个日期
        if process_papers(args.date):
            logger.info("论文语音生成完成")
            return 0
        else:
            logger.error("论文语音生成失败")
            return 1

if __name__ == "__main__":
    sys.exit(main()) 