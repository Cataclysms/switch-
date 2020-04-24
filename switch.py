import requests
import bs4
import re
import schedule
import time

REMAINING_SEC = 20#価格を取得する間隔
line = "https://notify-api.line.me/api/notify"
access_token = ''#LINEアクセストークン
headers = {'Authorization': 'Bearer ' + access_token}

def sendmessage(nmessage):
	message = nmessage
	payload = {'message': message}
	r = requests.post(line, headers=headers, params=payload,)

def get_price():
	source = ""#トラッキングしたい商品のURL(amazon)
	url = requests.get(source)
	soup = bs4.BeautifulSoup(url.text,features = "lxml")
	html = soup.select('.a-span12 span.a-color-price')
	if not html:
		html = soup.select('.a-color-base span.a-color-price')
	if str(html) == "[]":
		print("価格を取得できませんでした")
		return
	pricestr = str(html).replace(',','')
	priceint = re.sub(r'\D', '', pricestr)
	price = (int(priceint))
	print("指定された商品の現在価格:　"+str(price)+"円")
	if price < 25000 or price > 150000:#LINEに通知が行く条件
		sendmessage("\n現在の価格　"+str(price)+"\n"+source)

if __name__ == '__main__':
	get_price()
	schedule.every(REMAINING_SEC).seconds.do(get_price)
	while True:
		schedule.run_pending()
		time.sleep(1)