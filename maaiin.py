from bs4 import BeautifulSoup as bs
import requests
import openpyxl


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def get_links(html):
    soup = bs(html, 'html.parser')
    content = soup.find('div', class_='dj-items')
    data_list = content.find('div', class_='dj-items-table-smart')
    row = data_list.find('div', class_='dj-items-rows')
    posts = row.find_all('div', class_='item_row item_row0 item_new')
    links = []
    for post in posts:
        title = post.find('div', class_='item_content_in')
        print(title.text.strip())
        link = post.find('div', class_ = 'item_img_box_in').find('a').get('href')
        full_link = 'https://auto312.kg' + link
        links.append(full_link)

    return links

def get_data(html):
    soup = bs(html, 'html.parser')
    content = soup.find('div', class_='dj-item-in')
    box = content.find('div', class_='classifieds-desc-tab')
    title = content.find('div', class_='title_top info').text.strip()
    print(title)
    price = soup.find('span', class_='price_unit')
    print(f'{price.text.strip()}$')
    title_desc = box.find('div', class_='desc_content').text.strip()
    print(title_desc)
    years = soup.find('div', class_='custom_det_content')
    year = years.find('div', class_='row row___5')
    # print(year.text.strip())
    fuel_type = soup.find('div', class_='row row__').text.strip()
    # print(fuel_type)
    gearbox = soup.find('div', class_='row row___1')
    # print(gearbox.text.strip())
    engine_capacity = soup.find('div', class_='row row___2').text.strip()
    # print(engine_capacity)
   
    data = {
        'year': year,
        'fuel_type': fuel_type,
        'gearbox': gearbox,
        'engine_capacity': engine_capacity,
        'price': price,
    }

    return data

def get_last_page(html):
    soup = bs(html,'html.parser')
    wrap = soup.find('div',class_='pagination')
    page = wrap.find('ul')
    last = page.find('li', class_='pagination-end').find('a').get('href')

    return int(last[17:20])


def write_to_excel(data):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet['A1'] = 'Год выпуска'
    worksheet['B1'] = 'Тип топлива'
    worksheet['C1'] = 'Коробка передач'
    worksheet['D1'] = 'мощность движка'
    worksheet['E1'] = 'Цена'
    

    for i,item in enumerate(data, start=2):
        worksheet[f'A{i}'] = item['year']
        worksheet[f'B{i}'] = item['fuel_type']
        worksheet[f'C{i}'] = item['gearbox']
        worksheet[f'D{i}'] = item['engine_capacity']
        worksheet[f'E{i}'] = item['price']
    workbook.save('avt312.xlsx')


def main():
    URL = 'https://auto312.kg/cars.html'
    html = get_html(URL)
    links = get_links(html)
    last_page = get_last_page(html)
    print(last_page)
    for i in range(1,3):
        URL = 'https://auto312.kg/cars.html' + f'?start={i}'
        html = get_html(URL)
        links = get_links(html)
        for link in links:
            htm = get_html(link)
            get_data(htm)
            data = []

    write_to_excel(data)
    
if  __name__ == '__main__':
    main()
