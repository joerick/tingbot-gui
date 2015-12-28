import pygame
from .widget import Widget
from ..graphics import _topleft_from_aligned_xy


class Slider(Widget):
    def __init__(self,xy,size,align="center",parent=None,max_val=1.0,min_val=0.0,step=None,change_callback=None):
        """create a button with size and position specified by xy, size and align
        it will be a vertical slider if height is greater than width, otherwise horizontal
        max_val and min_val specify the maximum and minimum values respectively
        step specifies the step value, or 1/10 on the distance between max_val and min_val if zero or None
        change_callback is a function to call if the value changes
        """
        super(Slider,self).__init__(xy,size,align,parent)
        self.vertical = size[0] < size[1]
        self.max_val = max_val
        self.min_val = min_val
        if step:
            self.step = step
        else:
            self.step = (max_val-min_val)/10
        self.value = min_val
        self.pressed = False
        self.callback = change_callback
        
    def get_handle_size(self):
        (w,h) = self.size
        if self.vertical:
            return (w,w)
        else:
            return (h,h)
    
    def get_handle_position(self):
        (w,h) = self.size
        handle_size = self.get_handle_size()
        position = (self.value-self.min_val)/(self.max_val-self.min_val)
        position = max(min(position,1.0),0.0) #clip to be with max_val and min_val
        if self.vertical:
            position = (w/2,int(h-((h-handle_size[1])*position)+handle_size[1]/2))
        else:
            position = (int((w-handle_size[0])*position)+handle_size[0]/2,h/2)
        return position
    
    def draw_groove(self):
        (w,h) = self.size
        if self.vertical:
            start = (w/2,0)
            end = (w/2,h)
            width = w/5
        else:
            start = (0,h/2)
            end = (w,h/2)
            width = h/5
        pygame.draw.line(self.surface,(40,40,40),start,end,width)
        
    def draw_handle(self):
        position = self.get_handle_position()
        size = self.get_handle_size()
        pygame.draw.circle(self.surface,(200,200,200),position,size[0]/2)
    
    def draw(self):
        self.fill("black")
        self.draw_groove()
        self.draw_handle()
        
    def on_touch(self,xy,action):
        handle_size = self.get_handle_size()
        if self.pressed:
            if action=="move" or action=="up":
                if self.vertical:
                    pos = float(xy[1]-handle_size[1]/2)/(self.size[1]-handle_size[1])
                else:
                    pos = float(xy[0]-handle_size[0]/2)/(self.size[0]-handle_size[0])
                self.value = self.min_val+pos*(self.max_val-self.min_val)
                self.value = min(self.value,self.max_val)
                self.value = max(self.value,self.min_val)
                if self.callback:
                    self.callback(self.value)
                self.update()
        else:
            if action=="down":
                handle_pos = _topleft_from_aligned_xy(self.get_handle_position(),"center",handle_size,self.parent.size)
                handle_rect = pygame.Rect(handle_pos,handle_size)
                if handle_rect.collidepoint(xy):
                    self.pressed = True
                    
