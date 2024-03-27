# -*- coding: utf-8 -*-
"""
@Time: 2024/3/22 19:13
@Auth: kiei
@File: trust_calculator.py
@IDE: PyCharm
"""

from tkinter import *
from math import ceil

# 外观
root = Tk()
root.title("Trust Calculator")
# root.geometry('500x260+100+100')
# root["background"] = "#ffffff"
font_title = ('宋体', 20)
font_result = ('宋体', 16)
font_cross = ('黑体', 40)

needtrust = StringVar()
needtrust.set(f'需要0点信赖')  # 初始值
needdays = StringVar()
needdays.set(f'预计需要0天')

"""0. Title"""
row0 = 1
Label(root, text='信赖计算器', font=font_title,
      height=2, width=44).grid(row=row0, column=1, columnspan=5)
# Label(root, text='by kiei', justify='right',
#       height=1, width=10).grid(row=row0+1, column=4, pady=5)
"""
思路1.0: 12人以内的时候，把信赖最低12345个人放中枢和基建+刷关，10人刷关，比较用时，输出最长的天数。
        （假设内容过多，只能作为参考）
思路1.1: 模拟每一天的情况，用while语句更新每天的信赖变化。（但理智液只能默认day1用完，十分不方便）

思路1.1.1: 战斗（和理智液）理智以155为单位增加，避免了一次性加很多溢出浪费的情况 
"""
info = \
    f'刷信赖Tips：\n' \
    f'1. 刷关可以多带信赖未满的干员\n' \
    f'2. 中枢副手可以塞5个人\n' \
    f'3. 干员可以放在宿舍、加工站、\n' \
    f'   训练室等基建空位过夜\n\n' \
    f'计算说明：\n' \
    f'1. 没算活动期间150%信赖\n' \
    f'别问为什么，代码不会写(TT\n\n' \
    f'数据来源：prts.wiki\n' \
    f'反馈邮箱：331454670@qq.com\n' \
    # todo prts跳转

def copyfeedback():
    root.clipboard_clear()
    root.clipboard_append('331454670@qq.com')
    root.update()


Label(root, text=info,
      height=15, width=30, justify='left').grid(row=row0+2, column=1, padx=10, rowspan=5, columnspan=2)

# Label(root, text=info2,
#       justify='left').grid(row=row0+5, column=1, padx=10, columnspan=2)

Button(root, text='点此复制', command=copyfeedback
       ).grid(row=row0+6, column=2)




"""1. Input"""
row1 = row0 + 1 + 1
column1 = 2 + 1
# 未满的信赖
Label(root, text='请输入干员的信赖：\n(用“,”或“ ”分开，例：0,20,199)', anchor='e',
      height=2, width=30).grid(row=row1, column=column1, sticky='e', padx=0, pady=5, columnspan=2)

trust_var = StringVar()
# trust_entry = Entry(root, width=50, textvariable=trust_var)
# trust_entry.grid(row=row1, column=column1+1, padx=1, pady=5, sticky='w')
trust_entry = Text(root, width=20, height=4, font=('微软雅黑', 9))
scroll = Scrollbar(root, command=trust_entry.yview)
trust_entry.grid(row=row1, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)

# 理智液
Label(root, text='应急理智浓缩液(120)数量：', anchor='e',
      height=2, width=30).grid(row=row1+1, column=column1, sticky='e', columnspan=2)
Label(root, text='应急理智加强剂(80)数量：', anchor='e',
      height=2, width=30).grid(row=row1+2, column=column1, sticky='e', columnspan=2)
Label(root, text='应急理智小样(10)数量：', anchor='e',
      height=2, width=30).grid(row=row1+3, column=column1, sticky='e', columnspan=2)

sanity_var= [StringVar(), StringVar(), StringVar()]
sanity120_entry = Entry(root, width=20, textvariable=sanity_var[0])
sanity80_entry = Entry(root, width=20, textvariable=sanity_var[1])
sanity10_entry = Entry(root, width=20, textvariable=sanity_var[2])
sanity120_entry.insert(0, "0")
sanity80_entry.insert(0, "0")
sanity10_entry.insert(0, "0")
sanity120_entry.grid(row=row1+1, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)
sanity80_entry.grid(row=row1+2, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)
sanity10_entry.grid(row=row1+3, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)

# 各项目人数
Label(root, text='中枢副手(最上面)人数：', anchor='e',
      height=2, width=30).grid(row=row1+4, column=column1, sticky='e', columnspan=2)
Label(root, text='中枢副手(下面4个)人数：', anchor='e',
      height=2, width=30).grid(row=row1+5, column=column1, sticky='e', columnspan=2)
Label(root, text='基建刷信赖人数：', anchor='e',
      height=2, width=30).grid(row=row1+6, column=column1, sticky='e', columnspan=2)
Label(root, text='消耗理智作战带信赖人数：', anchor='e',
      height=2, width=30).grid(row=row1+7, column=column1, sticky='e', columnspan=2)

operaternum_var = [StringVar(), StringVar(), StringVar(), StringVar()]
centre_a_entry = Entry(root, width=20, textvariable=operaternum_var[0])
centre_b_entry = Entry(root, width=20, textvariable=operaternum_var[1])
dorm_entry = Entry(root, width=20, textvariable=operaternum_var[2])
combat_entry = Entry(root, width=20, textvariable=operaternum_var[3])
centre_a_entry.insert(0, "1")
centre_b_entry.insert(0, "4")
dorm_entry.insert(0, "5")
combat_entry.insert(0, "10")
centre_a_entry.grid(row=row1+4, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)
centre_b_entry.grid(row=row1+5, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)
dorm_entry.grid(row=row1+6, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)
combat_entry.grid(row=row1+7, column=column1+2, padx=10, pady=5, sticky='w', columnspan=1)



"""2. Calculate"""
t_list0 =[
    0,8,16,28,40,56,72,92,112,137,162,192,222,255,288,
    325,362,404,446,491,536,586,636,691,746,804,862,924,
    986,1052,1118,1184,1250,1316,1382,1457,1532,1607,1682,
    1757,1832,1917,2002,2087,2172,2257,2352,2447,2542,2637,
    2732,2840,2960,3080,3200,3320,3450,3580,3710,3840,3970,
    4110,4250,4390,4530,4670,4820,4970,5120,5270
]
t_list70 = [
    5420, 5575, 5730, 5885, 6040, 6195, 6350, 6505, 6660, 6815,
    6970, 7125, 7280, 7435, 7590, 7745, 7900, 8055, 8210, 8365,
    8520, 8675, 8830, 8985, 9140, 9295, 9450, 9605, 9760, 9915,
    10070, 10225, 10380, 10535, 10690, 10845, 11000, 11155, 11310,
    11465, 11620, 11775, 11930, 12085, 12240, 12395, 12550, 12705,
    12860, 13015, 13170, 13325, 13480, 13635, 13790, 13945, 14100,
    14255, 14410, 14565, 14720, 14875, 15030, 15185, 15340, 15495,
    15650, 15805, 15960, 16115, 16270, 16425, 16580, 16735, 16890,
    17045, 17200, 17355, 17510, 17665, 17820, 17975, 18130, 18285,
    18440, 18595, 18750, 18905, 19060, 19215, 19370, 19525, 19680,
    19835, 19990, 20145, 20300, 20455, 20610, 20765, 20920, 21075,
    21230, 21385, 21540, 21695, 21850, 22005, 22160, 22315, 22470,
    22625, 22780, 22935, 23090, 23245, 23400, 23555, 23710, 23865,
    24020, 24175, 24330, 24485, 24640, 24795, 24950, 25105, 25260,
    25415, 25570,
]
t_list = t_list0 + t_list70

t_dic = dict(zip([*range(0, 201)], t_list))
# point2percen = dict(zip(t_list, [*range(0, 201)]))


def get_long_list(*lst):
    return max(*lst, key=lambda v: len(v))

class Calculate:
    def __init__(self):
        pass

    # def get_trust(self):
    #     return trust_entry.get()

    def cal_trust(self, lst):
        """计算需要多少点信赖"""
        total = 0
        for t in lst:
            if int(t) < 70:
                total += 25570 - t_dic[int(t)]  # 总信赖 - 已有
            elif int(t) >= 70 and int(t) < 200:
                total += 155 * (200 - int(t))  # 155 * 差的等级数
        return total

# todo 活动期间1.5倍
    def cal_days(self):
        d = 0
        t = 0
        l = [int(x) for x in self.l]
        l.sort(reverse=True)  # max -> min

        # (1) 最低的放中枢副手+宿舍+刷关： 中枢副手(500 * 2) + 宿舍(100) + 理智(240) / 天
        tperd = 500 * 2 + 100 + 240  # trust per day
        days1 = (self.cal_trust([l[-1]]) - self.sanityplus) / tperd
        l.pop()
        if len(l) == 0:
            return ceil(days1)

        # (2-5) 放中枢b+宿舍+刷关：中枢b(100 * 2) + 宿舍(100) + 理智(240) / 天
        tperd = 125 * 2 + 100 + 240
        days2 = (self.cal_trust(l[-4:]) - self.sanityplus*min(len(l), 4)) / (tperd * min(len(l), 4))
        for i in range(4):
            try:
                l.pop()
            except:
                return max(ceil(days1), ceil(days2))

        # (6-10) 刷关：
        tperd = 240
        days3 = (self.cal_trust(l[-5:]) - self.sanityplus*min(len(l), 5)) / (tperd * min(len(l), 5))
        for i in range(5):
            try:
                l.pop()
            except:
                return max(ceil(days1), ceil(days2), ceil(days3))

        # (11+) 模糊估计：按日均4900计算：
        return (self.cal_trust(self.l) / 4900)

    def cal_old1(self):
        self.s = trust_entry.get(1.0, END)  # str
        self.sanityplus = 0
        try:
            if len(sanity10_entry.get()) > 0:
                self.sanityplus += int(sanity10_entry.get()) * 10
            if len(sanity80_entry.get()) > 0:
                self.sanityplus += int(sanity80_entry.get()) * 80
            if len(sanity120_entry.get()) > 0:
                self.sanityplus += int(sanity120_entry.get()) * 120
        except:
            needtrust.set('请输入数字，不要乱写！')
            return

        l1 = self.s.split('，')
        l2 = self.s.split(',')
        l3 = self.s.split(', ')
        l4 = self.s.split(' ')
        l5 = self.s.split('.')
        self.l = get_long_list(l1, l2, l3, l4, l5)
        needtrust.set(f'需要{self.cal_trust(self.l)}点信赖')
        needdays.set(f'预计需要{self.cal_days()}天')

    def cal(self):
        """计算、输出"""
        """1. 接受信息"""
        # 信赖序列
        self.s = trust_entry.get(1.0, END)  # str
        # 理智液
        self.sanityplus = 0
        self.centre_a, self.centre_b, self.dorm, self.combat = 1, 4, 5, 10
        try:
            if len(sanity10_entry.get()) > 0:
                self.sanityplus += int(sanity10_entry.get()) * 10
            if len(sanity80_entry.get()) > 0:
                self.sanityplus += int(sanity80_entry.get()) * 80
            if len(sanity120_entry.get()) > 0:
                self.sanityplus += int(sanity120_entry.get()) * 120
            if len(centre_a_entry.get()) > 0:
                assert int(centre_a_entry.get()) in [0, 1]
                self.centre_a = int(centre_a_entry.get())
            if len(centre_b_entry.get()) > 0:
                assert int(centre_b_entry.get()) in [1, 2, 3, 4]
                self.centre_b = int(centre_b_entry.get())
            if len(dorm_entry.get()) > 0:
                assert int(dorm_entry.get()) in [*range(20)]
                self.dorm = int(dorm_entry.get())
            if len(combat_entry.get()) > 0:
                assert int(centre_b_entry.get()) in [*range(13)]
                self.combat = int(combat_entry.get())
        except:
            needtrust.set('请输入数字，不要乱写！')
            return

        l1 = self.s.split('，')
        l2 = self.s.split(',')
        l3 = self.s.split(', ')
        l4 = self.s.split(' ')
        l5 = self.s.split('.')
        self.l = get_long_list(l1, l2, l3, l4, l5)
        del l1, l2, l3, l4, l5

        """2. 模拟计算"""
        needtrust.set(f'总共需要{self.cal_trust(self.l)}点信赖')
        # needdays.set(f'预计需要{self.cal_days()}天')
        l_update = [t_dic[int(i)] for i in self.l]  # % -> point
        l_update = self.simulate(l_update, centre_a=self.centre_a, centre_b=self.centre_b, dorm=self.dorm,
                                 combat=self.combat, sanityplus=self.sanityplus)
        days = 1
        # 移除信赖达到25570+的干员(如果有多个？)
        l_tmp = [x for x in l_update]
        for point in l_tmp:  # 直接迭代l_update，会导致序列变短，未遍历完整就结束了
            if point >= 25570:
                l_update.remove(point)

        while len(l_update) > 0:
            l_update = self.simulate(l_update, centre_a=self.centre_a, centre_b=self.centre_b, dorm=self.dorm,
                                     combat=self.combat)
            days += 1
            l_tmp = [x for x in l_update]
            for point in l_tmp:
                if point >= 25570:
                    l_update.remove(point)
        needdays.set(f'预计需要{days}天')


    def simulate(self, l, centre_a=1, centre_b=4, dorm=10, combat=10, sanityplus=0):
        """
        输入一个信赖序列，输出一天后的信赖变化
        :param l: 信赖点数序列。List[int]，len(l)<=12。
        :param centre_a: 中枢(top位置)干员数<=1
        :param centre_a: 中枢b1234干员数<=4
        :param dorm: 基建其他位置干员数<=20
        :param combat: 刷关带的干员数<=12
        :param sanityplus: 理智液总数
        :return: 输出一天后的信赖点数变化。List[int]
        """
        # assert len(l) <= 12, "输入序列过长，请输入长度在12以内的序列"
        l_point = [int(x) for x in l]
        l_point.sort()  # min->max
        n = len(l_point)
        # l_percen = l1  # 信赖值（%）
        # l_point = [t_dic[p] for p in l_percen]  # 信赖点数
        if combat:
            if l_point[min(combat-1, n-1)] + 240 + sanityplus >= 25570:
                # 如果一次性全加上去会满信赖，则分成若干个155计算
                # todo 这里还可以数学上化简（简化循环模拟）
                times, left = (240+sanityplus) // 155, (240+sanityplus) % 155  # 商和余数
                for ti in range(times):
                    for i in range(min(combat, n)):
                        l_point[i] += 155
                    l_point.sort()  # 刷够155换一次人
                for i in range(min(combat, n)):
                    l_point[i] += left
            else:
                for i in range(min(combat, n)):
                    l_point[i] += 240 + sanityplus

        if centre_a:
            l_point[0] += 500*2
        if centre_b:
            for i in range(1, min(centre_b+1, n)):
                # 以免序列不够长
                l_point[i] += 125*2
        if dorm:
            for i in range(min(dorm, n)):
                l_point[i] += 100

        # for idx in range(len(l_point)):
        #     x = l_point[idx]
            # x为现有信赖点数，求x对应的信赖值(%)
            # 在有序数组中插入一个x，求x的位置
            # for t in range(201):
            #     if x < t_dic[t]:
            #         break
            # l_percen[idx] = t-1

        return l_point





"""3. Output"""
row3 = row1 + 7 + 1
calculate = Calculate()
Button(root, text='确认', command=lambda: calculate.cal()
       ).grid(row=row3, column=column1+2, sticky='w')

# 结果框
# 需要信赖点
Label(root, textvariable=needtrust, font=(30),
      height=3, width=20).grid(row=row3+1, column=1, sticky='e', pady=5, columnspan=3)
# 需要天数
Label(root, textvariable=needdays, font=(30),
      height=3, width=20).grid(row=row3+1, column=4, sticky='w', padx=10, pady=5, columnspan=2)


root.mainloop()