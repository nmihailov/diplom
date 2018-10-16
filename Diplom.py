
# coding: utf-8

# In[6]:


import requests
import time
import json


def geturl(method):
    return 'https://api.vk.com/method/{method_name}'.format(method_name=method)


def groups_search(friends):
    for i in range(0, len(friends)):
        try:
            friend = friends[i]
            parameters = {
                'user_id': friend,
                'access_token': TOKEN,
                'v': '5.74'
            }
            responce = requests.get(geturl('groups.get'), parameters)
            friend_gr_list = responce.json()['response']['items']
            print('.')
            rez = list(set(group_list) & set(friend_gr_list))
            if len(rez) != 0:
                key = rez[0]
                group_dict[key] = group_dict[key] + 1 
            time.sleep(0.34)
        except KeyError:
            pass


def get_result(groups):
    for i in groups:
        params = {
            'group_id': i,
            'access_token': TOKEN,
            'v': '5.74'
        }
        responce1 = requests.get(geturl('groups.getById'), params)
        responce2 = requests.get(geturl('groups.getMembers'), params)
        name = responce1.json()['response'][0]['name']
        cnt = responce2.json()['response']['count']
        result_dictionary = {'name': name, 'gid': i, 'members_count': cnt}
        program_rezult.append(result_dictionary)
        time.sleep(0.34)


user = 'eshmargunov'
TOKEN = input('Введите токен пользователя eshmargunov: ')
params = {
    'user_ids': user,
    'access_token': TOKEN,
    'v': '5.74'
}
responce = requests.get(geturl('friends.get'), params)
friends_list = responce.json()['response']['items']

responce = requests.get(geturl('groups.get'), params)
group_list = responce.json()['response']['items']
group_dict = dict.fromkeys(group_list, 0)
groups_search(friends_list)

rez_groups = []
for key in group_dict.keys():
    if group_dict[key] == 0:
        rez_groups.append(key)
        
program_result = []
get_result(rez_groups)

with open('groups.json', 'w') as outfile:
    json.dump(program_result, outfile)

