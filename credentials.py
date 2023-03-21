import os


    

def credentials(instance):
    """Specify the instance you are working with:
    "e" - enterprise instance requires the following ENV  variables:
        ENTERPRISE_CANVAS_API_KEY
        ENTERPRISE_CANVAS_API_PATH
    
    "m" - moringa instance requires the following ENV variables:
        MORINGA_CANVAS_API_KEY
        MORINGA_CANVAS_API_PATH
        
    "a" - academyxi instance requires the following ENV   variables:
        AXI_CANVAS_API_KEY
        AXI_CANVAS_API_PATH
        
    "c" - consumer instance requires the following EN variables:
        CONSUMER_CANVAS_API_KEY
        CONSUMER_CANVAS_API_PATH
        
    "v" - vanguard instance requires the following EN variables:
        VANGUARD_CANVAS_API_KEY
        VANGUARD_CANVAS_API_PATH
    
    Args:
        instance (_type_): _description_

    Returns:
        _type_: _description_
    """
    if instance == 'e':
        instance = 'enterprise'
        API_KEY = os.getenv("ENTERPRISE_CANVAS_API_KEY")
        API_PATH = os.getenv("ENTERPRISE_CANVAS_API_PATH")
    if instance == 'm':
        instance = 'moringa'
        API_KEY = os.getenv("MORINGA_CANVAS_API_KEY")
        API_PATH = os.getenv("MORINGA_CANVAS_API_PATH")
    if instance == 'a':
        instance = 'academyxi'
        API_KEY = os.getenv("AXI_CANVAS_API_KEY")
        API_PATH = os.getenv("AXI_CANVAS_API_PATH")
    if instance == 'c':
        instance = 'consumer'
        API_KEY = os.getenv("CONSUMER_CANVAS_API_KEY")
        API_PATH = os.getenv("CONSUMER_CANVAS_API_PATH")
    if instance == 'v':
        instance = 'vanguard'
        API_KEY = os.getenv("VANGUARD_CANVAS_API_KEY")
        API_PATH = os.getenv("VANGUARD_CANVAS_API_PATH")
    return API_KEY, API_PATH