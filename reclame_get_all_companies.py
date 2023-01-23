#!/bin/python3
from bs4 import BeautifulSoup
import requests, multiprocessing, sys, json

requests.packages.urllib3.disable_warnings()

class Reclame_aqui_dump():

	def __init__(self):
		self.status_error = False
		self.company_id_range = list(range(1,300000))
		#self.company_id_range = list(range(0,5))
		self.dump()
	
	def company_max_value(self):
		# TODO: Checar se existe empresas novas
		return 114830

	def get(self,url):
		try:
			s = requests.Session()
			proxy_servers = {
			'http' : 'http://127.0.0.1:8081',
			'https' : 'http://127.0.0.1:8081'
			}
			s.proxies = proxy_servers
			s.timeout=5
			req = requests.Request(
				method='GET',
				url=url,
				headers={
				"Accept": "application/json",
				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
				"Origin":"https://www.reclameaqui.com.br"
				}
			)
			prep =  req.prepare()
			prep.url = url

			self.request = s.send(
				prep, verify=False
			)

			if(self.request.status_code==403):
				print("[!] Maybe being blocked?")
				exit()

		except Exception:
		  self.status_error = True
		return self.request.text

	def worker(self,company_id):
		file = open("todas_empresas3.txt", "a")  # append mode
		# set max loop

		#for index in range(0,500,25):
		url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/complains/?company={}&index=0&offset=25&order=created&orderType=desc".format(company_id)
		reclamacoes = json.loads(self.get(url))
		there_is_some_company_complain = bool(len(reclamacoes["data"]))

		if not there_is_some_company_complain:

			text = "[Nome] NULL | [ID] {}".format(company_id)
			file.write(text+" \n")
		else:
		#print("[{}] | [NULL?] {} [Len] {} ".format(company_id,there_is_some_company_complain,len(reclamacoes["data"])))
		#for claim in reclamacoes["data"]:
			text = "[Nome] {} | [ID] {}".format(reclamacoes["data"][0]["company"]["companyName"],company_id)
			file.write(text+" \n")

			#print ("[Company name] {} [Company id] {} [index] {}".format(reclamacoes[["company"]["companyName"],company_id,index))

	def dump(self):
		fire = multiprocessing.Pool(3)
		try:
			fire.map(
				self.worker, self.company_id_range
			)
			fire.close()
			fire.join()
		except UnboundLocalError:
			pass
		except KeyboardInterrupt:
			sys.exit(0)



def main():
	result = Reclame_aqui_dump()

if __name__ == "__main__":
	main()
