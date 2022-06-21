import requests
import json 
import time
import os
import importlib
from os.path import dirname, join, exists

# from .res.drawCard import Card, Box
from .res import drawCard
import hoshino
from hoshino import Service, log, priv, get_bot


# 程序初始化代码
curpath = dirname(__file__)
res_dir = join(curpath,'res/')
up_dir = join(curpath,'uppers/')

sv=Service(
    name='b站动态监视器-测试版',
    use_priv = priv.NORMAL,
    manage_priv = priv.ADMIN,
    visible=True,
    enable_on_default=True
)

# 该功能为Debug使用，生产前请禁用
@sv.on_prefix('测试动态')
async def bili_dy_from_id(bot,ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, "你没有权限这么做")
        return

    dyid = ev.message.extract_plain_text()
    if not dyid.isdigit():
        return        
    
    importlib.reload(drawCard)
    
    res = requests.get(url=f"http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={dyid}")

    dydetail = json.loads(res.text)
    with open(curpath+'/example_json_while_testing.json', 'w') as f:
        json.dump(dydetail, f, ensure_ascii=False)

    dylist = {"data":{"cards":[dydetail['data']['card']]}}

    dynamic = drawCard.Card(dylist)
    drawBox = drawCard.Box(650, 1200)

    dyimg, dytype = dynamic.draw(drawBox)
    if dytype == "转发":
                str_dytype = "转发了一条动态"
    else:
        str_dytype = f'发布了一个新{dytype}'

    msg = f"{dynamic.nickname} {str_dytype}, 点击连接直达：\n https://t.bilibili.com/{dynamic.dyidstr}  \n[CQ:image,file={dyimg}]"
    await bot.send(ev,msg)

@sv.on_prefix('测试up')
async def bili_dy_from_uid(bot,ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, "你没有权限这么做")
        return
        
    uid = ev.message.extract_plain_text()
    if not uid.isdigit():
        return        

    importlib.reload(drawCard)
    try:
        res = requests.get(url=f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}')
    except:
        return
    dylist = json.loads(res.text)
    with open(curpath+'/example_json_while_testing.json', 'w') as f:
        json.dump(dylist["data"]["cards"][0], f, ensure_ascii=False)
    dynamic = drawCard.Card(dylist) 
    drawBox = drawCard.Box(650, 1200)

    dyimg, dytype = dynamic.draw(drawBox)
    if dytype == "转发":
                str_dytype = "转发了一条动态"
    else:
        str_dytype = f'发布了一个新{dytype}'

    msg = f"{dynamic.nickname} {str_dytype}, 点击连接直达：\n https://t.bilibili.com/{dynamic.dyidstr}  \n[CQ:image,file={dyimg}]"
    await bot.send(ev,msg)

