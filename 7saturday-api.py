import os

import requests

start_index = 0
end_index = 400
gap = 20

# gather list data
data = []
while start_index < end_index:
    response = requests.get(f"https://discovery.7saturday.com/api/v1/top_influencers?filters=%7B%22start_index%22:{start_index},%22end_index%22:{start_index+gap},%22random_index%22:31%7D").json()
    print(f"from: {start_index} to: {start_index+gap}")
    data += response['popular_influencers']
    start_index += gap

#start writing
folder = os.path.join(os.getcwd(), "Core/Input")
os.chdir(folder)
f = open('new-input.txt', 'w', encoding='utf-8', newline='\r\n')

for influencer in data:
    print(influencer['username'])
    f.writelines(influencer['username'])
    f.write('\n')

f.close()
