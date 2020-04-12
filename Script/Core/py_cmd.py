from Script.Core import (
    flow_handle,
    main_frame,
    dictionaries,
    cache_contorl,
    game_config,
)

# 清除命令
clear_default_flow = flow_handle.clear_default_flow
# 绑定或重新绑定一个命令
bind_cmd = flow_handle.bind_cmd

# 输出命令
def pcmd(
    cmd_str: str,
    cmd_id: int,
    cmd_func=flow_handle.null_func,
    arg=(),
    kw={},
    normal_style="standard",
    on_style="onbutton",
):
    """
    打印一条指令
    Keyword arguments:
    cmd_str -- 命令对应文字
    cmd_id -- 命令数字
    cmd_func -- 命令函数
    arg -- 传给命令函数的顺序参数
    kw -- 传给命令函数的字典参数
    normal_style -- 正常状态下命令显示样式
    on_style -- 鼠标在其上的时候命令显示样式
    """
    cmd_str = dictionaries.handle_text(cmd_str)
    cmd_id = dictionaries.handle_text(f"{cmd_id}")
    cache_contorl.text_wait = float(game_config.text_wait)
    global last_char
    if len(cmd_str) > 0:
        last_char = cmd_str[-1:]
    flow_handle.print_cmd(cmd_str, cmd_id, cmd_func, arg, kw, normal_style, on_style)


# 获得一个没有用过的命令编号
unused_cmd_num = 500


def get_unused_cmd_num():
    """
    获得一个没有使用的命令编号，从500开始
    """
    global unused_cmd_num
    unused_cmd_num += 1
    return unused_cmd_num


# 清除命令，没有参数则清除所有命令
def clr_cmd(*number, clr_default_flow=True):
    """
    清楚绑定命令和默认处理函数
    Keyword arguments:
    number -- 清楚绑定命令数字
    clr_default_flow -- 是否同时清楚默认处理函数
    """
    if clr_default_flow == True:
        clear_default_flow()
    if number:
        flow_handle.cmd_clear(number)
    else:
        global unused_cmd_num
        unused_cmd_num = 500
        flow_handle.cmd_clear()


def focus_cmd():
    """
    使光标聚焦在命令输出框上
    """
    main_frame.inputbox.focus_force()