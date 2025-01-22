import os
import json
import datetime
import pytz
import requests
import logging
import argparse
from utils import setup_logger

# 设置日志记录器
logger = setup_logger()

def download_papers(date_str=None):
    """
    下载论文数据
    Args:
        date_str: 可选，指定要下载的日期，格式为YYYY-MM-DD。如果不指定，则使用当前日期。
    """
    try:
        # 如果没有指定日期，使用北京时间当前日期
        if date_str is None:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            current_time = datetime.datetime.now(beijing_tz)
            date_str = current_time.strftime('%Y-%m-%d')
        
        logger.info(f"正在获取 {date_str} 的论文数据")
        
        # 构建API URL
        url = f"https://huggingface.co/api/daily_papers?date={date_str}"
        
        # 发送请求
        response = requests.get(url)
        
        # 检查响应状态
        if response.status_code == 200:
            papers = response.json()
            if papers:
                # 只在有数据时创建文件
                os.makedirs('Paper_metadata_download', exist_ok=True)
                output_file = os.path.join('Paper_metadata_download', f"{date_str}.json")
                
                # 保存数据
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(papers, f, ensure_ascii=False, indent=2)
                logger.info(f"成功下载并保存了 {len(papers)} 篇论文的数据")
                return {"status": "success", "date": date_str}
            else:
                logger.warning(f"{date_str} 没有可用的论文数据")
                return {"status": "no_data", "date": date_str}
        else:
            logger.error(f"API请求失败: {response.status_code}")
            return {"status": "error", "date": date_str, "message": f"API请求失败: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"下载论文数据时发生错误: {str(e)}")
        return {"status": "error", "date": date_str, "message": str(e)}

def download_papers_in_range(start_date_str, end_date_str):
    """
    下载指定日期范围内的论文数据
    Args:
        start_date_str: 开始日期，格式为YYYY-MM-DD
        end_date_str: 结束日期，格式为YYYY-MM-DD
    Returns:
        dict: 包含每个日期下载结果的字典
    """
    try:
        # 验证日期格式
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            if start_date > end_date:
                logger.error("开始日期不能晚于结束日期")
                return {"status": "error", "message": "开始日期不能晚于结束日期"}
        except ValueError as e:
            logger.error(f"日期格式错误: {str(e)}")
            return {"status": "error", "message": f"日期格式错误: {str(e)}"}

        results = {}
        current_date = start_date
        while current_date <= end_date:
            current_date_str = current_date.strftime('%Y-%m-%d')
            logger.info(f"正在处理日期: {current_date_str}")
            result = download_papers(current_date_str)
            results[current_date_str] = result
            current_date += datetime.timedelta(days=1)

        return results

    except Exception as e:
        logger.error(f"下载日期范围内的论文数据时发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='下载HuggingFace每日论文数据')
    parser.add_argument('--date', type=str, help='指定要下载的日期 (YYYY-MM-DD格式)')
    parser.add_argument('--start_date', type=str, help='下载范围的开始日期 (YYYY-MM-DD格式)')
    parser.add_argument('--end_date', type=str, help='下载范围的结束日期 (YYYY-MM-DD格式)')
    args = parser.parse_args()

    # 处理日期范围下载
    if args.start_date and args.end_date:
        if args.date:
            logger.warning("同时指定了单个日期和日期范围，将优先处理日期范围")
        results = download_papers_in_range(args.start_date, args.end_date)
        if isinstance(results, dict):
            # 只有在有真正的错误时才返回错误状态码，没有数据不算错误
            if any(r.get("status") == "error" for r in results.values()):
                exit(1)
    else:
        # 使用指定的日期或默认使用当前日期
        result = download_papers(args.date)
        # 只有在有真正的错误时才返回错误状态码，没有数据不算错误
        if result["status"] == "error":
            exit(1)
    exit(0) 