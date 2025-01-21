import logging

def setup_logger():
    """
    设置并配置日志记录器
    Returns:
        logging.Logger: 配置好的日志记录器实例
    """
    # 创建日志记录器
    logger = logging.getLogger('paper_downloader')
    logger.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger 