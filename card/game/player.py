# coding:utf-8
import random
from Card import Card, reduce_ziyuan


class Player():
    def __init__(self, market, cardpile, name, nickname):
        self.nickname = nickname
        self.name = name
        self.ziyuan = {}  # 资源改为用dict存，1资源个数，5资源个数
        self.zise_ziyuan = 0
        self.wupin_card = {}
        self.score = 0
        self.state = 0
        self.market = market
        self.win = False
        self.card_pile = cardpile
        self.effect = []  # 影响效果，在各个阶段要考虑
        self.wupin_card_consider = None  # 抽到的物品卡，等待是否拿走的决定

    def is_win(self):
        hengzhi_count = 0
        for k, card in self.wupin_card.iteritems():
            if card.is_hengzhi:
                hengzhi_count += 1
        if hengzhi_count >= 7:
            self.win = True
            return True
        return False

    def run(self):
        # 摸牌，一张资源，一张物品（没卡怎么办？）
        # 资源卡必摸，如果摸物品，则不能买市场，否则可以买市场
        # 物品摸之后可以扔市场
        ziyuan = self.card_pile.get_a_ziyuan_card()
        wupin = self.card_pile.get_a_wupin_card()
        # 展示物品，提示是否购买

        # for循环：不断提示是否使用物品卡，如果结束回合，return
        # 使用物品卡
        # 结束回合

    def hengzhi(self):
        pass

    # 输出所有卡详细信息
    def show_all_card_with_detail(self):
        wupin_info = []
        for k in self.wupin_card:
            wupin_info += self.wupin_card[k].show_card_info()
        wupin_consider_info = self.wupin_card_consider.show_card_info()
        # 将两个info转成json传给用户


    # 弃牌，扔到市场（只对consider区域的牌有效）
    def drop_to_market(self, card_id, to_none=False):
        if to_none:
            self.wupin_card_consider = None
            return
        market = self.market
        self.wupin_card_consider.player = "market"
        market.wupin_card[card_id] = self.wupin_card_consider
        self.wupin_card_consider = None

    # 被弃牌，消失
    def drop_to_none(self, card_id):
        print("self.wupin_card", self.wupin_card)
        print("self.wupin_card[card_id]", self.wupin_card[card_id])
        self.score -= self.wupin_card[card_id].score
        self.wupin_card.pop(card_id)

    # 用牌，横放
    def use(self, card_id):
        self.wupin_card[card_id].is_hengzhi = True

    # 从consider区拿卡
    def get_card_from_consider(self, card_id):
        card = self.wupin_card_consider
        if card.id != card_id:
            print "error in get card from consider"
        card.player = self.name

        if self.get_total_ziyuan() < card.price or self.zise_ziyuan < card.zise_price:
            return u"你的资源不够了"
        reduce_ziyuan(card.price, self, self.card_pile)
        self.zise_ziyuan -= card.zise_price
        self.wupin_card[card.id] = card
        self.score += card.score
        self.wupin_card_consider = None
        return None

    # 从市场拿卡
    def get_card_from_market(self, card_id):
        card = self.market.wupin_card[card_id]
        card.player = self.name
        if self.get_total_ziyuan() < card.price or self.zise_ziyuan < card.zise_price:
            return u"你的资源不够了"
        reduce_ziyuan(card.price, self, self.card_pile)
        self.zise_ziyuan -= card.zise_price
        self.wupin_card[card.id] = card
        self.score += card.score
        self.market.wupin_card.pop(card_id)
        return None

    # 抽一张物品卡
    def get_a_wupin_card(self):
        cardpile = self.card_pile
        if len(cardpile.wupin_card.keys()) == 0:
            return u"牌堆里没有物品卡了"
        key_chosen = random.choice(cardpile.wupin_card.keys())
        card = cardpile.wupin_card[key_chosen]
        cardpile.wupin_card.pop(key_chosen)
        card.player = "consider"
        self.wupin_card_consider = card
        return None

    # 抽一张资源卡
    def get_a_ziyuan_card(self):
        cardpile = self.card_pile
        ziyuan_total_num = cardpile.get_total_ziyuan_count()
        if ziyuan_total_num == 0:
            return u"没有资源卡了"
        idx = random.randint(0, ziyuan_total_num - 1)
        if idx <= cardpile.get_ziyuan_count():
            # 抽到普通资源
            if idx <= cardpile.ziyuan["1"]:
                self.ziyuan["1"] += 1
                cardpile.ziyuan["1"] -= 1
            else:
                self.ziyuan["5"] += 1
                cardpile.ziyuan["5"] -= 1
        else:
            self.zise_ziyuan += cardpile.zise_ziyuan[idx - cardpile.get_ziyuan_count()]
            cardpile.zise_ziyuan.pop(idx - cardpile.get_ziyuan_count())
        return None

    def add_score(self, score):
        self.score += score
        return

    def sub_score(self, score):
        self.score -= score
        return

    def init_ziyuan(self):
        self.zise_ziyuan = 1
        self.ziyuan["1"] = 3
        self.ziyuan["5"] = 1
        return

    def get_total_ziyuan(self):
        return self.ziyuan["1"] + self.ziyuan["5"] * 5

    def stolen(self, card_id, stoler):
        card = self.wupin_card[card_id]
        self.wupin_card.pop(card_id)
        self.score -= card.score
        stoler.wupin_card[card_id] = card
        stoler.score += card.score
        card.is_hengzhi = False
        return

    def change_ziyuan(self, one, five, zise):
        self.ziyuan["1"] -= one
        self.ziyuan["5"] -= five
        self.zise_ziyuan -= zise
        for i in xrange(0, one + five + zise):
            self.get_a_ziyuan_card()
        return

    def add_ziyuan(self, one, five, zise):
        self.ziyuan["1"] += one
        self.ziyuan["5"] += five
        self.zise_ziyuan += zise
        return

    def del_ziyuan(self, one, five, zise):
        self.ziyuan["1"] -= one
        self.ziyuan["5"] -= five
        self.zise_ziyuan -= zise
        return
    
    def drop_ziyuan_random(self):
        total = self.ziyuan["1"] + self.ziyuan["5"] + self.zise_ziyuan
        if total == 0:
            return u"不能弃了，没了！"
        idx = random.randint(0, total-1)
        if idx < self.ziyuan["1"]:
            self.ziyuan["1"] -= 1
        elif idx < self.ziyuan["1"] + self.ziyuan["5"]:
            self.ziyuan["5"] -= 1
        else:
            self.zise_ziyuan -= 1
        return

    def stolen_ziyuan(self, stoler, is_drop):
        total = self.ziyuan["1"] + self.ziyuan["5"] + self.zise_ziyuan
        if total == 0:
            return u"不能抽了，没了！"
        idx = random.randint(0, total-1)
        if idx < self.ziyuan["1"]:
            self.ziyuan["1"] -= 1
            if not is_drop:
                stoler.ziyuan["1"] += 1
        elif idx < self.ziyuan["1"] + self.ziyuan["5"]:
            self.ziyuan["5"] -= 1
            if not is_drop:
                stoler.ziyuan["5"] += 1
        else:
            self.zise_ziyuan -= 1
            if not is_drop:
                stoler.zise_ziyuan += 1
        return