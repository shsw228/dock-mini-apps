import lvgl as lv
import display_driver

# The name of the application to be displayed on the menu
NAME = "Check Alive"

# A file path or data (bytes type) of the logo image for this app.
# If not specified, the default icon will be applied.
ICON = ""

# LVGL widgets
scr = None
label1 = None
label2 = None
label3 = None

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
    global scr, label1, label2, label3
    
    
    get_user_setting()
    scr = lv.obj()
    lv.screen_active().set_flex_flow(lv.FLEX_FLOW.COLUMN)
    #lv.screen_active().set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER)
    label1 = lv.label(scr)
    label2 = lv.label(scr)
    label3 = lv.label(scr)
    update_label()
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
