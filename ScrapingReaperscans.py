import os
import time

import requests
from bs4 import BeautifulSoup

cookies = {
    'cf_clearance': 'egAky99QQWzm9ZS9.80xbKT0XyAQG2RTcGx9rI2VjE8-1719058245-1.0.1.1-PvYmhoFrNALZhIbmq2ylDA_YMLOYtzRG7enbXtWVbmyEykn.W3joPFzIxn5Dj0wu3mMjOwtLVBzOChSXa2zDrg',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,uk-UA;q=0.7,uk;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'PHPSESSID=573291f46f82c1edf2cc8a3c0cafdfcc; _gid=GA1.2.897475407.1718978831; wpmanga-reading-history=W3siaWQiOjE2NjA1LCJjIjoiMTQ1MzMiLCJwIjoxLCJpIjoiIiwidCI6MTcxODk5NjY3MX0seyJpZCI6MTQzODMsImMiOiIxNDU5OSIsInAiOjEsImkiOiIiLCJ0IjoxNzE4OTk2MjE2fV0%3D; _gat_gtag_UA_179244075_1=1; _ga_7VJ26C3FEG=GS1.1.1719055613.2.1.1719055654.0.0.0; _ga=GA1.1.1937209930.1718805390; _ga_Z51MXHD9LG=GS1.1.1719055613.2.1.1719055654.0.0.0; cf_clearance=n7muVNPT1aR1IpLBkqYM2EOnNmFW0BN32CfC8SkPIOg-1719055654-1.0.1.1-gyLJrFfANfjIvRBYZ1pC2KxfDIMAEx.Wmj.324uCObLLm3Zp_rx7QyhKUm8N4D_t_iJKk4wFueDrLpAZAXHhGQ',
    'priority': 'u=0, i',
    'referer': 'https://reaperscans.fr/serie/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"126.0.6478.114"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.114", "Google Chrome";v="126.0.6478.114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"12.7.5"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}


def find_all_chapitre(response_find_all_chapitre):
    result_dict_chapitre = {}
    soup = BeautifulSoup(response_find_all_chapitre.text, 'lxml')
    find_all_chapitre_in_site = soup.find_all('div', class_='chapter-link')
    for chapitre in find_all_chapitre_in_site:
        chapitre_number = chapitre.find('p').text
        result_dict_chapitre[chapitre_number] = chapitre.find('a')['href']
    return result_dict_chapitre


def find_all_images_links_and_download(dict_with_all_collected_chapitre, directory_name):
    global cookies, headers
    for key, value in dict_with_all_collected_chapitre.items():
        counter = 0
        path = os.path.join(f"data/{directory_name}/", key)
        os.makedirs(path)
        response_image = requests.get(value, headers=headers, cookies=cookies, timeout=10)
        while response_image.status_code == 403:
            print('--------------------------------')
            cookies['cf_clearance'] = input('Send a new cf_clearance in cookies for continue: ')
            response_image = requests.get(value, headers=headers, cookies=cookies, timeout=10)
        soup_images = BeautifulSoup(response_image.text, 'lxml')
        all_links_images = soup_images.find_all('img', class_='wp-manga-chapter-img')
        print(f'Created a folder {key}')
        len_all_links = len(all_links_images)
        for link_img in all_links_images:
            link_img = link_img['src'].replace('\n', '')
            counter += 1
            print(f'Downloading {counter} of {len_all_links} images')
            img_data = requests.get(link_img, headers=headers, cookies=cookies, timeout=20)
            while img_data.status_code == 403:
                print('--------------------------------')
                cookies['cf_clearance'] = input('Send a new cf_clearance in cookies for continue: ')
                img_data = requests.get(link_img, headers=headers, cookies=cookies, timeout=20)
                time.sleep(2)
                with open(f'data/{directory_name}/{key}/image{counter}.jpg', 'wb') as handler:
                    handler.write(img_data.content)
            else:
                time.sleep(2)
                with open(f'data/{directory_name}/{key}/image{counter}.jpg', 'wb') as handler:
                    handler.write(img_data.content)


links = ['https://reaperscans.fr/serie/the-little-lady-behind-the-scenes/']
for link in links:
    directory = link.split('/')[-2]
    print(f'Work with {directory}')
    response = requests.get(link, headers=headers, cookies=cookies, timeout=10)
    while response.status_code == 403:
        print('--------------------------------')
        cookies['cf_clearance'] = input('Send a new cf_clearance in cookies for continue: ')
        response = requests.get(link, headers=headers, cookies=cookies, timeout=10)
    all_chapitre = find_all_chapitre(response)
    find_all_images_links_and_download(all_chapitre, directory)









