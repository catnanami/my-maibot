from nonebot import get_driver
from .config import Config
import random
from datetime import date
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import on_command
import json,random 
global_config = get_driver().config
config = Config.parse_obj(global_config)

participant_list=[]
song_list=[]
hidden_list=[]
name_list=[]
guess_list=[]
game=0
'''
async def get_part_list():
    str='目前参与开字母的成员有：\n'
    for member in participant_list:
        info=str(await Bot.get_stranger_info(user_id=member))
        user_name=json.loads(info.replace("'", '"'))['nickname']
        str+=user_name+'\n'
    return str
'''
with open('.\\namelist_EN.json',encoding='utf-8') as info:
    infos=json.load(info)
    for element in infos:
        name_list.append(element.get('song_name'))
    info.close()

def rp(string):
    str0=string
    str0=str0.replace(' ','')
    str0=str0.replace('开','')
    str0=str0.replace('歌','')
    str0=str0.replace('名','')
    for i in range(0,len(str0)):
         char=str0[i].lower()
         str0=str0[:i]+char+str0[(i+1):]
    return str0

def new_game():
    global song_list,hidden_list,guess_list
    song_list=random.sample(name_list,10)
    hidden_list=[]
    guess_list=[]
    for element in song_list:
        print(element)
        str0=''
        for each_str in element:
            if each_str==' ':
                str0+=' '
            else:
                str0+='*'
        print(str0)
        hidden_list.append(str0)
    pass

def show():
    string='已经开过的字母有：'
    flag=False
    for element in guess_list:
        if flag:
            string+='、'
        else:
            flag=True
        string+=element
    string+='\n当前开字母进度：\n'
    for element in hidden_list:
        string+=element+'\n'
    return string

def update(char):
    global hidden_list,song_list
    for i in range(0,10):
        print(song_list[i])
        for j in range(0,len(song_list[i])):
            if (hidden_list[i][j]=='*')&((song_list[i][j]==char.upper())|(song_list[i][j]==char.lower())):
                hidden_list[i]=hidden_list[i][:j]+song_list[i][j]+hidden_list[i][(j+1):]
                print(hidden_list[i])

def match(string):
    global hidden_list,song_list
    string=rp(string)
    print(string)
    for i in range(0,10):
        if string==rp(song_list[i]):
            hidden_list[i]=song_list[i]
    pass


def judge_end():
    global hidden_list,song_list
    for i in range(0,10):
        if song_list[i]!=hidden_list[i]:
            return False
    return True 
    pass
'''
participate=on_command("p")

@participate.handle()
async def partin_function(bot: Bot, event: Event):
    global game
    part_user=event.get_user_id()
    if game==1:
        await participate.finish(Message('游戏已经开始了喂(#`O′)'))
        pass
    if part_user in participant_list:
        await participate.finish(Message('你已经报名过了Σ(°ロ°)不可以重复报名哦~'))
        pass
    else:
        participant_list.append(part_user)
        message='报名成功~\n目前参与开字母的成员有（按开字母顺序）：\n'
        for member in participant_list:
            info=str(await bot.get_stranger_info(user_id=member))
            user_name=json.loads(info.replace("'", '"'))['nickname']
            message+=user_name+'\n'
        await participate.finish(Message(message))
        pass
'''
start=on_command('start',aliases={'kai','开始','开始吧','快开'})

@start.handle()
async def start_function(bot:Bot,event: Event):
    global game
    if game==1:
        await start.finish(Message('游戏已经开始了喂(#`O′)'))
        pass
    game=1
    new_game()
    message='游戏开始了喔~\n'+show()
    await start.finish(Message(message))
    pass

guess=on_keyword(['开字母'],priority=20)

@guess.handle()
async def guess_function(bot:Bot,event: Event):
    global game,guess_list,game
    if game==0:
        await guess.finish(Message('游戏还没开始呢Σ(°ロ°)'))
        pass
    dialog=event.get_plaintext()
    char=''
    for each_char in dialog:
        if each_char not in ['开','字','母',' ']:
            char=each_char
            break
    guess_list.append(char)
    update(char)
    info=str(await bot.get_stranger_info(user_id=event.get_user_id()))
    user_name=json.loads(info.replace("'", '"'))['nickname']
    message=user_name+'开出了字母'+char+'\n'
    message+=show()
    if judge_end():
        message+='\n游戏结束啦~大家真是太厉害了呢~'
        game=0
    await guess.finish(Message(message))
    pass

guess2=on_keyword(['开歌名'],priority=30)

@guess2.handle()
async def guess2_function(bot:Bot,event: Event):
    global game
    if game==0:
        await guess.finish(Message('游戏还没开始呢Σ(°ロ°)'))
        pass
    dialog=event.get_plaintext()
    match(dialog)
    message=show()
    if judge_end():
        message+='\n游戏结束啦~大家真是太厉害了呢~'
        game=0
    await guess2.finish(Message(message))

