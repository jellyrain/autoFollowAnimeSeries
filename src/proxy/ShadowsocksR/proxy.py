import os
import socket
import time


def start(ssr_dict, local_address: str = '127.0.0.1', local_port: int = 1080, udp: int = 0) -> None:
    """启动 ShadowsocksR 代理

    :param ssr_dict: SSR 服务器配置
    :param local_address: 本地地址
    :param local_port: 本地端口
    :param udp: UDP 转发
    :return: None
    """
    cmd_str = 'bin/ShadowsocksR.exe'
    cmd_str += '-s ' + ssr_dict['server']  # 服务器地址
    cmd_str += '-p ' + str(ssr_dict['server_port'])  # 服务器端口
    cmd_str += '-k ' + ssr_dict['password']  # 密码
    cmd_str += '-m ' + ssr_dict['method']  # 加密方式
    cmd_str += '-O ' + ssr_dict['protocol']  # 协议
    cmd_str += '-G ' + ssr_dict['protocol_param']  # 协议参数
    cmd_str += '-o ' + ssr_dict['obfs']  # 混淆
    cmd_str += '-g ' + ssr_dict['obfs_param']  # 混淆参数
    cmd_str += '-b ' + local_address  # 本地地址
    cmd_str += '-l ' + str(local_port)  # 本地端口
    cmd_str += '-u ' + str(udp)  # UDP 转发

    os.system(cmd_str)


def is_valid_connect(server: str, port: int) -> tuple[bool, str]:
    """测试服务器和端口和本地是否连通

    :param server: 服务器地址
    :param port:  服务器tcp端口
    :return: connect: True or False,表示是否可以连接
             delay: 本地到目标服务器tcp连接延迟
    """
    server_addr = (server, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    start_time = time.time()
    try:
        s.connect(server_addr)
        end_time = time.time()
    except Exception as e:
        s.close()
        return False, '∞'
    else:
        delay = round(end_time - start_time, 2) * 1000
        return True, str(delay)


def get_proxys(local_address: str = '127.0.0.1', local_port: int = 1080) -> dict[str, str]:
    """获取代理字典

    :param local_address: 本地地址
    :param local_port: 本地端口
    :return: 代理字典
    """
    return {
        'http': f'socks5://{local_address}:{local_port}',
        'https': f'socks5://{local_address}:{local_port}',
    }


__all__ = ['start', 'is_valid_connect', 'get_proxys']
