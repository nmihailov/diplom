
# coding: utf-8

# In[87]:


from pprint import pprint
import requests
import time
import json
from urllib.parse import urlencode


# In[88]:


user = 'eshmargunov'
TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


def url(method):
    
    return 'https://api.vk.com/method/{method_name}'.format(method_name = method)


params = {
    'user_ids': user,
    'access_token': TOKEN,
    'v': '5.74'
}

responce = requests.get(url('friends.get'), params)
friends_list = responce.json()['response']['items']

params = {
    'user_ids': user,
    'access_token': TOKEN,
    'v': '5.74'
}

responce = requests.get(url('groups.get'), params)
group_list = responce.json()['response']['items']
group_dict = dict.fromkeys(group_list, 0)
# print(group_dict)
# print(group_dict[151498735])


# In[89]:


# %%time
for i in range(0, len(friends_list)):
    try:
        friend = friends_list[i]
        parameters = {
        'user_id': friend,
        'access_token': TOKEN,
        'v': '5.74'
        }
        responce = requests.get(url('groups.get'), parameters)
        friend_gr_list = responce.json()['response']['items']
        print('.')
        rez = list(set(group_list) & set(friend_gr_list))
        if len(rez) != 0:
            key = rez[0]
            group_dict[key] = group_dict[key] + 1 
#             print(group_dict)
#         print(friend_gr_list)
        time.sleep(0.34)
    except KeyError:
        pass
    
rez_groups = []
for key in group_dict.keys():
    if group_dict[key] == 0:
        rez_groups.append(key)


# In[90]:


# print(rez_groups)
program_rezult = []
for i in rez_groups:
    params = {
        'group_id': i,
        'access_token': TOKEN,
        'v': '5.74'
    }

    responce1 = requests.get(url('groups.getById'), params)
    responce2 = requests.get(url('groups.getMembers'), params)
    name = responce1.json()['response'][0]['name']
    
    cnt = responce2.json()['response']['count']
    d = {'name': name, 'gid': i, 'members_count': cnt}
    program_rezult.append(d)
    
    time.sleep(0.34)
    
# print(program_rezult)
with open('groups.json', 'w') as outfile:
    json.dump(program_rezult, outfile)

