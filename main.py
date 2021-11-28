import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType

from cities import Cities

vk_session = vk_api.VkApi(token="32bf367218403d428a603d16a2dd495f6cfc3862a9a7b5ef8bad3d40cba9aad0c056ceda36f265107aea5")
longpoll = VkLongPoll(vk_session)


correct_cities = ['Новосибирск', 'Красноярск', 'Курск', 'Кемерово', 'Оренбунг', 'Гамбург']
players_in_game = []
active_games = []


def send_message(id, message):
    vk_session.method("messages.send", {"user_id": id,
                                        "message": message,
                                        "random_id": 0})


def is_message(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me


def is_play_game(event):
    game_command = ['начали', "let's go", 'города']
    return event.text.lower() in game_command


def kill_game(game):
    user_ids = game.user_ids
    active_games.pop(active_games.index(game))
    players_in_game.remove(user_ids[0])
    players_in_game.remove(user_ids[1])


def is_player_step(self, user_id):
    return user_id == self.user_ids[self.current_step]


def main():
    user_in_queue = None
    for event in longpoll.listen():
        if is_message(event):
            if is_play_game(event):
                if user_in_queue is None:
                    send_message(event.user_id, 'Вы встали в очередь на игру в города!')
                    user_in_queue = event.user_id
                elif event.user_id != user_in_queue:
                    send_message(user_in_queue, 'Мы нашли вам оппонента')
                    send_message(event.user_id, 'Оппонент уже ожидает вас!')
                    active_games.append(Cities(user_in_queue, event.user_id))
                    players_in_game.append(user_in_queue)
                    players_in_game.append(event.user_id)
                    first_user = active_games[-1].user_ids[active_games[-1].current_step]
                    send_message(first_user, 'Вы ходите первый! Назовите город на любую букву.')
                    user_in_queue = None
            elif event.user_id in players_in_game:
                bad = False
                igra = None
                for game in active_games:
                    if event.user_id in game.user_ids:
                        if game.user_ids.index(event.user_id) != game.current_step:
                            bad = True
                            break
                        else:
                            igra = game
                if bad:
                    send_message(event.user_id, 'Сейчас не ваш ход!')
                    continue
                if not igra.is_correct_first_char(event.text[0].lower()):
                    send_message(event.user_id, 'Вы назвали город не на ту букву и проиграли! Игра окончена!')
                    send_message(igra.user_ids[1 - igra.current_step], 'Вы победили!')
                    kill_game(igra)
                city = event.text
                user1 = igra.user_ids[0]
                user2 = igra.user_ids[1]
                if user1 != event.user_id:
                    user1, user2 = user2, user1
                if not igra.is_unused_city(city):
                    send_message(user1, 'Ты проиграл, потому что назвал уже названый город')
                    send_message(user2, 'Ты выйграл')
                    kill_game(igra)
                if igra in active_games:
                    do_step(user2, city)
                    send_message(user2, f'Твой ход. Ходишь на букву: {igra.last_char}.\n'
                                    f'Был назван город: {igra.used_cities[-1]}')

def do_step(user_id, city):
    for igra in active_games:
        if user_id in igra.user_ids:
            igra.current_step = 1 - igra.current_step
            igra.change_last_char(city)
            igra.used_cities.append(city.lower())
            break
    
main()
