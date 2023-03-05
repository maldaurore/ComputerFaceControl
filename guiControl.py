import pyautogui as gui


## Scrolls down the window the mouse is currently on.
def scrollDown():
    
    gui.scroll(-250)
    gui.scroll(-250)
    gui.scroll(-250)


## Scrolls up the window
def scrollUp():
    
    gui.scroll(250)
    gui.scroll(250)
    gui.scroll(250)
    
    
## Zoom in with a combination of control key and mouse scroll   
def zoomIn():
    
    gui.keyDown('ctrl')
    gui.scroll(250)
    gui.scroll(250)
    gui.scroll(250)
    gui.keyUp('ctrl')
    
    
# Travel between windows
def  windowMenu():
    
    gui.keyDown('altleft')
    gui.keyDown('tab')
    gui.keyUp('tab')

# Travel to the next window in the window menu
def nextWindow():
    
    gui.press('tab')

# Releases the window menu when the eyebrows are not longer raised. 
def releaseMenu():
    
    gui.keyUp('altleft')
    
    
def scrollLeft():
    
    gui.press('left')
    gui.press('left')
    gui.press('left')
    gui.press('left')
    gui.press('left')
    
    
def scrollRight():
    
    gui.press('right')
    gui.press('right')
    gui.press('right')
    gui.press('right')
    gui.press('right')
    
