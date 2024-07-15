import lvgl as lv
import logging
from .ping_utils import ping
import uasyncio as asyncio

# The name of the application to be displayed on the menu
NAME = "Check Alive"

# A file path or data (bytes type) of the logo image for this app.
# If not specified, the default icon will be applied.
ICON = ""
logger = logging.getLogger('check_alive')
# LVGL widgets
scr = None
label1 = None
label2 = None
label3 = None
resultLabel1 = None
resultLabel2:Label = None
resultLabel3:Label = None

# value
result1 = False
result2 = False
result3 = False

# Setting params
ip1 = None
ip2 = None
ip3 = None
DEFAULT_FREQUENCY = 1

frequency = DEFAULT_FREQUENCY

app_mgr = None
ping_now = False

def get_user_setting():
    global ip1, ip2, ip3, frequency
    
    ip1 = str(app_mgr.config().get("device1", "No value"))
    ip2 = str(app_mgr.config().get("device2", "No value"))
    ip3 = str(app_mgr.config().get("device3", "No value"))
    frequency = int(app_mgr.config().get("frequency", 0))
    
async def on_stop():
    # User triggered to leave this app, all features should be deactivated
    print('on_stop')

async def on_start():
    # User triggered to enter this app, all features should be activated
    print('on_start')
    global scr, label1, label2, label3, result1, result2, result3

    # スタイルを定義し、パディングを設定
    style = lv.style_t()
    style.init()
    style.set_pad_all(10)  # 全てのパディングを10に設定
    
    get_user_setting()
    scr = lv.obj()
    container = lv.obj(scr)
    container.set_size(lv.pct(100), lv.pct(50))
    container.add_style(style,0)
    
    container2 = lv.obj(scr)
    container2.set_size(lv.pct(100), lv.pct(50))
    resultLabel1 = lv.label(container2)
    resultLabel1.set_text(str(result1))
    resultLabel2 = lv.label(container2)
    resultLabel2.set_text(str(result2))
    resultLabel3 = lv.label(container2)
    resultLabel3.set_text(str(result3))
    
    container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    container2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    container2.align_to(container, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
    label1 = lv.label(container)
    label2 = lv.label(container)
    label3 = lv.label(container)
    update_label()
    
    
    hosts = [] # 初期化
    hosts = [ip1, ip2, ip3]  # Pingするホストのリスト
    tasks = [ping(host, count=4) for host in hosts]
    results = await asyncio.gather(*tasks)
    for result, host in zip(results, hosts):
        print(f"{host} results: {result}")
        if host == ip1:
            print(f"This is ip1")
        if host == ip2:
            print(f"This is ip2")
        if host == ip3:
            print(f"This is ip3")
        
    update_ping_status()

    lv.scr_load(scr)
        
    

async def on_boot(apm):
    global app_mgr
    app_mgr = apm

async def on_resume():
    get_user_setting()
    update_label()
    
    
def update_label():
    global label1, label2, label3, ip1, ip2, ip3
    if label1:
        label1.set_text(ip1)
    if label2:
        label2.set_text(ip2)
    if label3:
        label3.set_text(ip3)

def update_ping_status():
    global resultLabel1, resultLabel2, resultLabel3
    if resultLabel1:
        resultLabel1.set_text(str(result1))
    if resultLabel2:
        resultLabel2.set_text(str(result2))
    if resultLabel3:
        resultLabel3.set_text(str(result3))

def get_settings_json():
    return {
        "title":"Ping to your local devices",
        "form": [  
        {
            "type": "input",
            "default": "1",
            "caption": "PingFrequency:",
            "name": "frequency",
            "attributes": {"maxLength": 5, "placeholder": "Ping your device every {input} minutes."}
        },
        {
            "type": "input",
            "default": "",
            "caption": "Device1:",
            "name": "device1",
            "attributes": {"maxLength": 15, "placeholder": "Enter device ip(192.168.0.0)"}
        },
        {
            "type": "input",
            "default": "",
            "caption": "Device2:",
            "name": "device2",
            "attributes": {"maxLength": 15, "placeholder": "Enter device ip(192.168.0.0)"}
        },
        {
            "type": "input",
            "default": "",
            "caption": "Device3:",
            "name": "device3",
            "attributes": {"maxLength": 15, "placeholder": "Enter device ip(192.168.0.0)"}
        }]
    }



