import os


    
class Credentials:
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
    
    def __init__(self, instance):
        if instance == 'e':
            self.instance = 'enterprise'
            self.API_KEY = os.getenv("ENTERPRISE_CANVAS_API_KEY")
            self.API_PATH = os.getenv("ENTERPRISE_CANVAS_API_PATH")
        if instance == 'm':
            self.instance = 'moringa'
            self.API_KEY = os.getenv("MORINGA_CANVAS_API_KEY")
            self.API_PATH = os.getenv("MORINGA_CANVAS_API_PATH")
        if instance == 'a':
            self.instance = 'academyxi'
            self.API_KEY = os.getenv("AXI_CANVAS_API_KEY")
            self.API_PATH = os.getenv("AXI_CANVAS_API_PATH")
        if instance == 'c':
            self.instance = 'consumer'
            self.API_KEY = os.getenv("CONSUMER_CANVAS_API_KEY")
            self.API_PATH = os.getenv("CONSUMER_CANVAS_API_PATH")
        if instance == 'v':
            self.instance = 'vanguard'
            self.API_KEY = os.getenv("VANGUARD_CANVAS_API_KEY")
            self.API_PATH = os.getenv("VANGUARD_CANVAS_API_PATH")