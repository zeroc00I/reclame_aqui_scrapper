#!/bin/python3
from bs4 import BeautifulSoup
import requests, multiprocessing, sys, json, optparse

requests.packages.urllib3.disable_warnings()

def menu():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--threads', dest="threads", help='100',default=5)
    parser.add_option('-i', '--company_id', dest="company_id", help='1337')
    parser.add_option('-o', '--output', dest="output", help='output.txt')

    options, args = parser.parse_args()

    if not options.company_id:
    	print("[!] Company ID parameter is missing")
    	print("[-] Exiting...")
    	exit()

    globals().update(locals())

class Reclame_aqui_dump():

	def __init__(self):
		self.fetched_complains = 0
		self.status_error = False
		self.company_id_range = list(range(1,3000))
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
		file = open("reclamacoes_"+options.company_id, "a")  # append mode

		for index in range(0,2000,100):
			url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/complains/?company={}&index={}&offset=100&order=created&orderType=desc".format(company_id,index)
			reclamacoes = json.loads(self.get(url))
			there_is_some_company_complain = bool(len(reclamacoes["data"]))

			if not there_is_some_company_complain:

				print("[!] Reclaims not found on offset {}".format(offset))
				print("[-] Exiting...")
				exit()
			else:
				self.fetched_complains += len(reclamacoes["data"])
				print("[+]  Reclamações coletadas: {}".format(fetched_complains))
				for claim in reclamacoes["data"]:
					text = "[Descrição] {}".format(claim["description"])
					file.write(text+" \n")

	def dump(self):
		menu()
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
