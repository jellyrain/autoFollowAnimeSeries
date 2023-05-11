import base64


def parse_b64decode(base64_string: str) -> str:
    # 解析 base64 字符串 b64decode
    base64_string += '=' * (4 - len(base64_string) % 4)
    return base64.b64decode(base64_string).decode('utf-8')


def parse_urlsafe_b64decode(base64_string: str) -> str:
    # 解析 base64 字符串 urlsafe_b64decode
    base64_string += '=' * (4 - len(base64_string) % 4)
    return base64.urlsafe_b64decode(base64_string).decode('utf-8')


def parse_base64(base64_string: str) -> str:
    # 解析 base64 字符串 b64decode 或 urlsafe_b64decode 没办法必须二次封装
    try:
        return parse_b64decode(base64_string)
    except Exception as e:
        return parse_urlsafe_b64decode(base64_string)


def parse_ssr(ssr_url: str) -> dict[str, str]:
    # 解析 ssr 链接
    server, port, protocol, method, obfs, password = parse_base64(ssr_url[6:]).split(':')
    query = {item.split('=')[0]: item.split('=')[1] for item in password.split('/?')[1].split('&')}
    return {
        'remarks': parse_base64(query.get('remarks', '')),  # 备注
        'server': server,  # 服务器地址
        'server_port': int(port),  # 服务器端口
        'method': method,  # 加密方式
        'password': parse_base64(password.split('/?')[0]),  # 密码
        'port_password': None,  # 端口密码
        'protocol': protocol,  # 协议
        'protocol_param': parse_base64(query.get('protoparam', '')),  # 协议参数
        'obfs': obfs,  # 混淆
        'obfs_param': parse_base64(query.get('obfsparam', '')),  # 混淆参数
        'group': parse_base64(query.get('group', '')),  # 分组
        'additional_ports': {},  # 额外端口
        'additional_ports_only': False,  # 仅额外端口
        'udp_timeout': 120,  # UDP 超时
        'udp_cache': 64,  # UDP 缓存
        'fast_open': False,  # 快速打开
        'verbose': False,  # 详细
        'connect_verbose_info': 0,  # 连接详细信息
        'connect': 0,  # 连接
        'ssr_url': ssr_url  # SSR 链接
    }


def parse_subscribe(subscribe_url: str) -> list[dict[str, str]]:
    # 解析订阅链接
    ssr_list = []
    for ssr_url in parse_base64(subscribe_url).split('\n'):
        if ssr_url.startswith('ssr://'):
            ssr_list.append(parse_ssr(ssr_url))
    return ssr_list


__all__ = ['parse_ssr', 'parse_subscribe']
