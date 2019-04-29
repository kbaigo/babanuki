import random
import numpy as np
import pandas as pd
import feather 

#ゲームプレイヤーを定義
def registerPlayers(player_number):
    return [[] for i in range(player_number)]

#デッキ生成
def createDeck():
    deck = [str(card) for card in range(1, 14) for i in range(4)]
    deck += ['Joker']
    return deck

#カード配布
def distributeCard(players_list, deck):
    random.shuffle(deck)
    while(len(deck) != 0):
        for player in players_list:
            if len(deck) == 0:
                break
            player += [deck[0]]
            deck.pop(0)

#カードを捨てる処理
def discardOwnCards(player):
    player_number = len(player)
    #手札に重複がなければ終了
    if len(set(player)) == player_number:
        return

    for i in range(player_number):
        for j in range(i + 1, player_number):
            if player[i] == player[j]:
                delete_card = player[i]
                player.remove(delete_card)
                player.remove(delete_card)
                discardOwnCards(player)
                return

#カードを引く処理

def drawCard(players_list, be_drawn_player, drawing_player):
    card = random.choice(players_list[be_drawn_player])
    players_list[be_drawn_player].remove(card)
    players_list[drawing_player].append(card)
    return

def skipWinner(players_list, player):
    player %= len(players_list)
    if len(players_list[player]) != 0:
        return player
    
    return skipWinner(players_list, player+1)

def checkParity(players_list):
    return ['even' if (len(player) % 2) == 0 else 'odd' for player in players_list]

def checkWinner(players_list, winners):
    for i, player in enumerate(players_list):
        if len(player) == 0:
            if not i in winners:
                winners.append(i)
                return i
    return 'nobody wins'

def game(players_list):
    
    #ゲーム開始
    turn = 0
    winners = []
    result_dict = {}
    
    #天和チェック
    tenho = checkWinner(players_list, winners)
    if type(tenho) is not str: print('Tenho!!')

    while(True):

        #カードを引く処理
        be_drawn_player = skipWinner(players_list, turn)
        drawing_player = skipWinner(players_list, be_drawn_player+1)
        drawCard(players_list, be_drawn_player, drawing_player)

        #引かれたプレイヤーがカードを捨てる処理
        discardOwnCards(players_list[be_drawn_player])
        checkWinner(players_list, winners)
        #引いたプレイヤーがカードを捨てる処理
        discardOwnCards(players_list[drawing_player])
        checkWinner(players_list, winners)

        #ゲーム終了チェック
        if len(winners) == len(players_list) - 1:
            winners.append(players_list.index(['Joker']))
            break
        turn = drawing_player
        

    for i, winner in enumerate(winners):
        result_dict['rank_{}'.format(i+1)] = winner

    return result_dict

def sortParity3(players_list, parity_str):
    assert(parity_str == 'eeo' or parity_str == 'oee')

    if(parity_str == 'eeo'):
        return
    if(parity_str == 'oee'):
        players_list[0], players_list[2] = players_list[2], players_list[0]
        return

def run3players(parity_str):
    player_number = 3
    players_list = registerPlayers(player_number)
    deck = createDeck()
    distributeCard(players_list, deck)
    for player in players_list:
        discardOwnCards(player)
    sortParity3(players_list, parity_str)
    
    return game(players_list)

if __name__ == '__main__':
    data_list = []

    for i in range(10000):
        parity = 'eeo' if (i % 2 == 0) else 'oee'
        result = run3players(parity)
        result['game_id'] = i + 1
        result['parity'] = parity
        data_list.append(result)
    
    data_df = pd.DataFrame(data_list)
    data_df.to_feather('./bin/game_result.feather')