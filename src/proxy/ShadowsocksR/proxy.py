import signal
import socket
import sys
import time

from src.proxy.ShadowsocksR.shadowsocks import asyncdns, daemon, tcprelay, udprelay, eventloop


def start(ssr_dict, local_address: str = '127.0.0.1', local_port: int = 1080, timeout: int = 300, workers: int = 1,
          dns_ipv6: bool = False) -> None:
    """在Windows操作系统平台开启shadowsocksr代理

            :param dns_ipv6: 是否支持ipv6
            :param workers: 加密级别
            :param timeout: 启动延迟
            :param local_port: 本地监听端口
            :param local_address: 本地监听地址
            :type ssr_dict: shadowsocksr 节点信息字典
    """
    ssr_dict['local_address'] = local_address
    ssr_dict['local_port'] = local_port
    ssr_dict['timeout'] = timeout
    ssr_dict['workers'] = workers

    if not dns_ipv6:
        asyncdns.IPV6_CONNECTION_SUPPORT = False

        try:
            daemon.daemon_exec(ssr_dict)
            dns_resolver = asyncdns.DNSResolver()
            tcp_server = tcprelay.TCPRelay(ssr_dict, dns_resolver, True)
            udp_server = udprelay.UDPRelay(ssr_dict, dns_resolver, True)
            loop = eventloop.EventLoop()
            dns_resolver.add_to_loop(loop)
            tcp_server.add_to_loop(loop)
            udp_server.add_to_loop(loop)

            def handler(signum, _):
                tcp_server.close(next_tick=True)
                udp_server.close(next_tick=True)

            signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

            def int_handler(signum, _):
                sys.exit(1)

            signal.signal(signal.SIGINT, int_handler)
            daemon.set_user(ssr_dict.get('user', None))
            loop.run()
        except Exception as e:
            sys.exit(1)


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
    return {
    'http': f'socks5://{local_address}:{local_port}',
    'https': f'socks5://{local_address}:{local_port}',
}

__all__ = ['start', 'is_valid_connect', 'get_proxys']
