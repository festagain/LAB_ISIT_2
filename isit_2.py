import matplotlib.pyplot as plt
import AUTH
import scipy as sp
from pyvis.network import Network
import vk_api
import jinja2


#Авторизация в VK API
def two_factor():
    # Двухфакторная аутентификация
    key = input("Enter authentication code: ")
    return key,True


def get_friends_ids(vk, user_id):
    try:
        friends_ids = vk.friends.get(user_id=user_id)['items']
        return friends_ids
    except Exception as e:
        print(f"Error: {e}")
        return []


login = AUTH.login
password = AUTH.password
vk_session = vk_api.VkApi(login, password, auth_handler=two_factor,app_id=2685278)

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()

# ID пользователя, друзей которого мы хотим получить
user_id = '275549140'

# Получаем ID друзей пользователя
friends_ids = get_friends_ids(vk, user_id)

# Создаем граф
nt = Network()

# Добавляем вершины графа
nt.add_node(user_id, color="red")
nt.add_nodes(friends_ids, color=["green"]*len(friends_ids))
# Добавляем ребра графа для друзей пользователя
for friend_id in friends_ids:
    nt.add_edge(user_id, friend_id)


    # Получаем ID друзей друзей и добавляем их в граф
    friends_of_friend_ids = get_friends_ids(vk, friend_id)

    if len(friends_of_friend_ids) == 0:
        continue
    nt.add_nodes(friends_of_friend_ids, color=["blue"]*len(friends_of_friend_ids))

    # # Добавляем ребра графа для друзей друзей
    for foaf_id in friends_of_friend_ids:
        nt.add_edge(friend_id, foaf_id)
# Рисуем граф
nt.save_graph("11.html")