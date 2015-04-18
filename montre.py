#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import time
TIME_FORMAT='%Y'
REFRESH_RATE_MS=50

class Montre(tk.Canvas):
    mapped_stick={
            '0':0b1110111,
            '1':0b0100100,
            '2':0b1011101,
            '3':0b1101101,
            '4':0b0101110,
            '5':0b1101011,
            '6':0b1111011,
            '7':0b0100101,
            '8':0b1111111,
            '9':0b1101111,
        }
    #mapped_stick_rel_pos={
    #        0:(10,0,110,10,),
    #        1:(0,10,10,110,),
    #        2:(110,10,120,110,),
    #        3:(10,110,110,120,),
    #        4:(0,120,10,220,),
    #        5:(110,120,120,220,),
    #        6:(10,220,110,230,),
    #    }
    mapped_polygon={
            0:(
                    0,
                    0,
                    100,
                    0,
                    90,
                    10,
                    10,
                    10,
                ),
            1:(
                    0,
                    0,
                    10,
                    10,
                    10,
                    90,
                    0,
                    100,
                ),
            2:(
                    100,
                    0,
                    100,
                    100,
                    90,
                    90,
                    90,
                    10,
                ),
            3:(
                    10,
                    95,
                    90,
                    95,
                    100,
                    100,
                    90,
                    105,
                    10,
                    105,
                    0,
                    100,
                ),
            4:(
                    0,
                    100,
                    10,
                    110,
                    10,
                    190,
                    0,
                    200,
                ),
            5:(
                    100,
                    100,
                    100,
                    200,
                    90,
                    190,
                    90,
                    110,
                ),
            6:(
                    10,
                    190,
                    90,
                    190,
                    100,
                    200,
                    0,
                    200,
                ),
       }
    def __init__(
            self,
            master=None,
        ):
        tk.Canvas.__init__(
                self,
                master,
                bg='#222',
                width=450,
                height=220,
            )
        self.last_year=None
        self.pack()
        self.init_digits()
        self.auto_refresh(REFRESH_RATE_MS)
    def init_digits(self):
        self.digit={}
        for i in range(4):
            for stick in range(7):
                rel_coord=list(Montre.mapped_polygon[stick])
                abs_coord=[]
                while not rel_coord == []:
                    abs_coord.append(rel_coord.pop(0)+110*i+10)
                    abs_coord.append(rel_coord.pop(0)+10)
                self.digit.setdefault(
                        i,
                        {},
                    )[stick]=self.create_polygon(
                            tuple(abs_coord),
                            width=0,
                            fill='#FFF',
                        )
    def refresh_year(self,year):
        if year==self.last_year:
            return
        new_sticks={i:Montre.mapped_stick[year[i]] for i in range(min(4,len(year)))}
        for i,bits in new_sticks.items():
            bitstr=str(bin(bits))[2:][::-1]
            for j in range(7):
                try:
                    if bitstr[j]=='1':
                        color='#FFF'
                    elif bitstr[j]=='0':
                        color='#000'
                except IndexError:
                    color='#000'
                _,_,_,_,old_color=self.itemconfig(self.digit[i][j])['fill']
                if old_color==color:
                    continue
                if old_color=='#FFF' and color=='#000':
                    shades=['#%X%X%X' % (c,c,c) for c in range(15,-1,-1)]
                elif old_color=='#000' and color=='#FFF':
                    shades=['#%X%X%X' % (c,c,c) for c in range(16)]
                else:
                    shades=[color]
                self.smooth_change(self.digit[i][j],shades,10)
        self.last_year=year
    def smooth_change(
            self,
            item,
            shades,
            pause,
        ):
        if len(shades)==0:
            return
        shade=shades.pop(0)
        self.itemconfigure(
                item,
                fill=shade,
            )
        self.after(
                pause,
                self.smooth_change,
                item,
                shades,
                pause,
            )
    def auto_refresh(
            self,
            ms,
        ):
        cur_year=time.strftime(TIME_FORMAT)
        self.refresh_year(cur_year)
        self.after(
                ms,
                self.auto_refresh,
                ms,
            )
if __name__ == '__main__':
    bruce=tk.Tk()
    bruce.title('le temps n\'existe pas')
    bruce.geometry('450x220-0+0')
    montre=Montre(
            master=bruce,
       )
    bruce.mainloop()
