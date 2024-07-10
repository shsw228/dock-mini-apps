# The name of the application to be displayed on the menu
NAME = "Life Cycle"

# A file path or data (bytes type) of the logo image for this app.
# If not specified, the default icon will be applied.
ICON = ""

async def on_stop():
    # User triggered to leave this app, all features should be deactivated
    print('on_stop')

async def on_start():
    # User triggered to enter this app, all features should be activated
    print('on_start')
    
async def on_boot(apm):
    print('on_boot')

async def on_create():
    print('on create')
    
async def on_pause():
    print('on_pause')
    
async def on_resume():
    print('on_resume')
    
async def on_running_foreground():
    print('on_running_foreground')
    
async def on_running_background():
    print('on_running_background')
    
async def on_destroy():
    print('on_destroy')
