import requests
import json
import bs4 
from bs4 import *
import lxml
import random
from pypresence import Presence
from art import *
from colorama import init
from colorama import Fore, Back, Style
from pyfiglet import figlet_format
from termcolor import cprint,colored
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import subprocess
import os
import sys
import logging
import sys
import csv
import time 
from datetime import datetime
import uuid
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
class Main:
	def __init__():
		pass

	@classmethod
	def clearconsole(self):
		clear = lambda: os.system('cls')
		clear()
	@classmethod
	def LoadJson(self,folder,file):
		try:
			with open('{}/{}'.format(str(folder),str(file))) as e:
				file = json.load(e)
				return file
		except Exception as e:
			print(e)
			return 'Folder/File Not Found!'
	@classmethod
	def LoadProxies(self,folder,file):
		a = []
		try:
			with open('{}/{}'.format(str(folder),str(file))) as e:
				proxies = e.read().splitlines()
				for i in proxies:
					proxy = i.split(':')
					try:
						proxy = {'http':'http://{}:{}@{}:{}'.format(proxy[2],proxy[3],proxy[0],proxy[1]),
								'https':'https://{}:{}@{}:{}'.format(proxy[2],proxy[3],proxy[0],proxy[1])}
					except:
						proxy = {'http':'{}:{}'.format(proxy[0],proxy[1]),
								'https':'{}:{}'.format(proxy[0],proxy[1])}

					a.append(proxy)

			if a == []:
				return None
			else:
				return a


		except Exception as e:
			print(e)
			return 'No Proxy File Found.'
	
	@classmethod
	def LoadTasks(self,folder,file):
		with open('{}/{}'.format(folder,file),'r') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			tasks = {}
			task_num = 0


			for task in csv_reader:
				task_num += 1
				try:
					task_object = {
						'TaskProfile':task[0],
						'Product':task[1],
						'SKU':task[2],
						'Size':task[3]
					}

					tasks[str(task_num)] = task_object
				except Exception as e:
					print(e)
					input('')

			return tasks

	@classmethod
	def get_proxy(self,obj):
		self.proxies = obj
		if self.proxies == None:
			return None
		else:
			proxy = self.proxies[random.randint(0,len(self.proxies)-1)]
			return proxy

	@classmethod
	def fprint(self,message,color):
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")

		print(colored('['+str(current_time)+'] '+'{}'.format(message),'{}'.format(color)))

	@classmethod
	def filter_proxies(self,folder,file):
		with open('{}/{}'.format(folder,file)) as e:
			proxies = e.read().splitlines()
			for i in proxies:
				proxy = i.split(':')

				proxy = {
					'http':'http://{}:{}@{}:{}'.format(proxy[2],proxy[3],proxy[0],proxy[1]),
					'https':'https://{}:{}@{}:{}'.format(proxy[2],proxy[3],proxy[0],proxy[1])
				}

				try:
					response = requests.get('https://www.supplystore.com.au/',proxies=proxy)
					print(i)
				except:
					pass

	
class Supplystore:

	
	init()
	def __init__(self,task,tasknum):
		self.token = ''
		self.config = Main.LoadJson('Supplystore','config.json')
		self.proxies = Main.LoadProxies('Supplystore','proxies.txt')
		self.profiles = self.LoadProfiles('Supplystore','profiles.csv')
		self.delay = int(self.config['delay'])
		self.tasknum = str(tasknum)


		self.session = requests.Session()
		self.proxy = Main.get_proxy(self.proxies)

		self.sku = None
		self.title = None
		self.color = None
		self.quantity = None
		self.size = None
		self.varSku = None
		self.access = None
		self.product = task['Product']



		self.login_email = self.profiles[task['TaskProfile']]['SS_Login']
		self.login_password = self.profiles[task['TaskProfile']]['SS_Password']
		self.first_name = self.profiles[task['TaskProfile']]['FName']
		self.last_name = self.profiles[task['TaskProfile']]['LName']
		self.address = self.profiles[task['TaskProfile']]['Address']
		self.suburb = self.profiles[task['TaskProfile']]['Suburb']
		self.state = self.profiles[task['TaskProfile']]['State']
		self.postcode = self.profiles[task['TaskProfile']]['PCode']
		self.phone = self.profiles[task['TaskProfile']]['Phone']

		if self.login():
			if self.cart_product():
				if self.shipping():
					if self.payment():
						if self.send_webhook(self.title,self.sku,self.size,'Supplystore CC [Restock Mode]',self.tasknum,self.access,self.product):
							print('Webhook Sent.')
							input()




	def send_webhook(self,title,sku,size,module,tasknum,access,product):
			config = Main.LoadJson('Supplystore','config.json')

			webhook = config['webhook']
			webhook = DiscordWebhook(url=str(webhook))
			embed = DiscordEmbed(title=str(title), description=None, color=242424,url=str(product))
			embed.add_embed_field(name='SKU',value=str(sku),inline=False)
			embed.add_embed_field(name='SIZE',value=str(size),inline=True)
			embed.add_embed_field(name='MODULE',value=str(module),inline=False)
			embed.set_author(name='Supplystore')
			# set footer
			embed.set_footer(text='SNKRLab CLI - Helping members make money',icon_url='https://media.discordapp.net/attachments/782532739001614347/787653010142396446/SNKRLAB_21.png?width=333&height=333')

			# set timestamp (default is now)
			embed.set_timestamp()

			# add fields to embed
			embed.add_embed_field(name='Task', value=str(tasknum))
			embed.add_embed_field(name='Manual Checkout', value='[Click me]({})'.format(str(access)))
			embed.set_thumbnail(url='https://www.supplystore.com.au/images/items/'+str(sku)+'/t_1.jpg')

			webhook.add_embed(embed)

			response = webhook.execute()
			return True
	def LoadProfiles(self,folder,file):
		with open('{}/{}'.format(folder,file),'r') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			profiles = {}

			for profile in csv_reader:
				try:
					profile_object = {
						'FName':profile[1],
						'LName':profile[2],
						'Email':profile[3],
						'Address':profile[4],
						'Suburb':profile[5],
						'State':profile[6],
						'PCode':profile[7],
						'Phone':profile[8],
						'CCNum':profile[9],
						'CCExp':profile[10],
						'CC_CVV':profile[11],
						'SS_Login':profile[12],
						'SS_Password':profile[13]
					}
					profiles[str(profile[0])] = profile_object
				except Exception as e:
					print(e)
					input('')

			return profiles	


	def login(self):
		logged = False
		while not logged:
			try:
				response = self.session.get('https://www.supplystore.com.au/shop/login.aspx',proxies=self.proxy)
			except Exception as e:
				print(e)
				Main.fprint('Proxies Banned - Rotating','red')
				self.proxy = Main.get_proxy(self.proxies)
				time.sleep(int(self.delay))
				continue	

			if response.status_code == 200:
				Main.fprint('Logging in...','green')
				
				soup = BeautifulSoup(response.content,'lxml')

				try:

					viewstate = soup.find('input',attrs={'id':'__VIEWSTATE'})['value']
					viewstategen = soup.find('input',attrs={'id':'__VIEWSTATEGENERATOR'})['value']
				except Exception as e:
					Main.fprint('Error getting viewstate','red')
					time.sleep(int(self.delay))
					continue


				self.get_token()
				if self.token == '':
					Main.fprint('Captcha Bank Server Broken - Restart Captcha Server and Try Again','red')
					break

				data = {
					'__EVENTTARGET': '',
					'__EVENTARGUMENT': '',
					'__VIEWSTATE': str(viewstate),
					'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$PageContentPlaceholder$loginForm$UserName': str(self.login_email),
					'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$PageContentPlaceholder$loginForm$Password': str(self.login_password),
					'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$PageContentPlaceholder$loginForm$RedirectUrl': '/',
					'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$PageContentPlaceholder$loginForm$Login': 'Login',
					'g-recaptcha-response': str(self.token),
					'__VIEWSTATEGENERATOR': str(viewstategen)
				}

				tries = 0

				try:
					response = self.session.post('https://www.supplystore.com.au/shop/login.aspx',data=data,proxies=self.proxy,allow_redirects=True)
				except Exception as e:
					Main.fprint('Proxies Banned - Rotating','red')
					time.sleep(int(self.delay))
					continue
				logged_in = False
				while not logged_in:
					if tries < 5:
						if response.url == 'https://www.supplystore.com.au/':
							Main.fprint('Successfully Logged in...','green')	
							logged_in = True
							return logged_in
						else:
							Main.fprint('Failed to login','red')
							time.sleep(int(self.delay))
							tries = tries + 1
					else:
						Main.fprint('Too many failed attempts - Getting new session','red')
						self.session = requests.Session()
						self.proxy = Main.get_proxy(self.proxies)
						logged_in = True
						continue
			elif response.status_code == 502:
				Main.fprint('Bad Gateway [502]','red')
				time.sleep(int(self.delay))
	def stock_check(self):
		in_stock = False

		while not in_stock:
			try:
				response = requests.get(str(self.product),proxies=Main.get_proxy(self.proxies))
			except Exception as e:
				print(e)
				Main.fprint('Proxies Banned - Rotating','red')
				time.sleep(int(self.delay))
				continue

			if response.status_code == 200:
				Main.fprint('Fetching Product Stock','yellow')

				soup = BeautifulSoup(response.content,'lxml')


				self.sku = soup.find('input',attrs={'name':'sku'})['value']
				self.title = soup.find('div',attrs={'class':'columns large-4 product-copy'}).find('h3').text

				t = soup.find('select',attrs={'id':'Form_Form_Options_Size'})
				stock = t.find_all('option')
				self.color = soup.find('select',attrs={'id':'Form_Form_Options_Color'}).find('option')['value']

				self.quantity = soup.find('input',attrs={'id':'Form_Form_Available'})['value']
				available = []

				for i in stock:
					if 'Out' in str(i.text):
						pass
					else:
						available.append(i['value'])

				if available == []:
					Main.fprint('OUT OF STOCK','yellow')
					time.sleep(int(self.delay))
				else:
					Main.fprint('Stock Detected','green')

					atc_button = soup.find('input',attrs={'id':'Form_Form_action_doform'})
					if atc_button == None:
						Main.fprint('Cannot ATC','red')
						time.sleep(int(self.delay))
					else:
						Main.fprint('ATC Available','green')
						self.size = available[random.randint(0,len(available))-1]
						
						s = soup.find('select',attrs={'id':'variantSku'})
						p = s.find_all('option')
						for i in p:
							if str(i['size']) == self.size:
								self.varSku = str(i['value'])

						return True

			elif response.status_code == 502:
				Main.fprint('Bad gateway [502]','red')
			elif response != 200:
				Main.fprint('Unkown error [{}}'.format(response.status_code),'red')
	def cart_product(self):
		stock = self.stock_check()
		if stock:
			carted = False
			while not carted:
				self.get_token()
				if self.token == '':
					Main.fprint('Captcha Bank Broken - Please restart your captcha bank','red')
					input()
					break
				data = {

					'sku': str(self.sku),
					'variantSku': str(self.varSku),
					'varSize': str(self.size),
					'varColor': str(self.color),
					'quantityAvailable': str(self.quantity),
					'quantityInput': '1',
					'action_doform': 'Add To Cart',
					'g-recaptcha-response':str(self.token)
				}

				try:
					response = self.session.post(str(self.product),proxies=self.proxy,data=data)
				except:
					Main.fprint('Proxies Banned - Rotating','red')
					self.proxy = Main.get_proxy(proxies)
				if response.status_code == 200:
					Main.fprint('Carting Product','yellow')

					if response.url == 'https://www.supplystore.com.au/shop/checkout/cart.aspx':
						Main.fprint('Product Carted [{}]'.format(self.size),'green')
						carted = True
						return carted
					else:
						Main.fprint('Failed to cart product','red')
						time.sleep(int(self.delay))

				else:
					print(colored(Config.get_time()+'Unkown Website Error ['+str(response.status_code)+']','red'))
					time.sleep(3)
	def shipping(self):
		con = False
		
		while not con:
			self.get_token()
			if self.token == '':
				Main.fprint('Captcha Bank Broken - Please restart','red')
				input()
				break


			data = {
				'quantityInput_0': '1',
				'quantityInput_1': '1',
				'checkout': 'Checkout Now',
				'g-recaptcha-response':str(self.token)
			}
			try:
				response = self.session.post('https://www.supplystore.com.au/shop/checkout/cart.aspx',data=data,proxies=self.proxy)
			except:
				Main.fprint('Proxies Banned - Rotating','red')
				self.proxy = Main.get_proxy(proxies)
				time.sleep(int(self.delay))

			if response.url == 'https://www.supplystore.com.au/shop/checkout/address.aspx':
				Main.fprint('Proceeding to shipping...','yellow')
				con = True
			else:
				Main.fprint('Failed Getting Shipping...','red')
				time.sleep(int(self.delay))
				continue

		ship_1 = False
		while not ship_1:
			self.get_token()
			if self.token == '':
				Main.fprint('Captcha Bank Broken - Please restart','red')
				input()
				break
			data = {
				'firstNameInput': str(self.first_name),
				'lastNameInput': str(self.last_name),
				'phoneInput': str(self.phone),
				'mobileInput': str(self.phone),
				'emailInput': str(self.login_email),
				'attentionInput': '',
				'companyInput': '',
				'line1Input': str(self.address),
				'cityInput': str(self.suburb),
				'stateInput': str(self.state),
				'postalCodeInput': str(self.postcode),
				'countryInput': '8',
				'shipment_firstNameInput': str(self.first_name),
				'shipment_lastNameInput': str(self.last_name),
				'shipment_attentionInput': '',
				'shipment_companyInput': '',
				'shipment_line1Input': str(self.address),
				'shipment_cityInput': str(self.suburb),
				'shipment_stateInput': str(self.state),
				'shipment_postalCodeInput': str(self.postcode),
				'shipment_countryInput': '8',
				'action_register': 'Proceed',
				'g-recaptcha-response':str(self.token)
			}
			try:
				response = self.session.post('https://www.supplystore.com.au/shop/checkout/address.aspx',data=data,proxies=self.proxy)
			except:
				Main.fprint('Proxies Banned - Rotating','red')
				self.proxy = Main.get_proxy(proxies)
				time.sleep(int(self.delay))
				continue
			if response.url == 'https://www.supplystore.com.au/shop/checkout/shipping.aspx':
				Main.fprint('Submitting Shipping... [1]','green')
				ship_1 = True
			else:
				Main.fprint('Failed to submit shipping... [1]','red')
				time.sleep(int(self.delay))
				continue

		ship_2 = False
		while not ship_2:
			self.get_token()
			if self.token == '':
				Main.fprint('Captcha bank broken - Please restart','red')
				input()
				break

			data = {
				'shippingMethodInput': '8',
				'action_doShipping': 'Proceed to payment',
				'g-recaptcha-response':str(self.token)
			}
			try:
				response = self.session.post('https://www.supplystore.com.au/shop/checkout/shipping.aspx',data=data,proxies=self.proxy)
			except:
				Main.fprint('Proxies Banned - Rotating','red')
				self.proxy = Main.get_proxy(proxies)
				time.sleep(int(self.delay))
			if response.url == 'https://www.supplystore.com.au/shop/checkout/payment.aspx':
				Main.fprint('Proceeding to Payment...','green')
				ship_2 = True
				return ship_2

			else:
				Main.fprint('Failed proceeding to payment...','red')
				time.sleep(int(self.delay))
	def payment(self):


		pay = False

		while not pay:
			self.get_token()
			if self.token == '':
				Main.fprint('Captcha Bank Broken - Please try restart','red')
				input()
				break

			data = {
				'paymentMethodInput': '10',
				'action_doPayment': 'Proceed',
				'g-recaptcha-response':str(self.token)
			}
			try:
				response = self.session.post('https://www.supplystore.com.au/shop/checkout/payment.aspx',data=data,proxies=self.proxy)
			except:
				Main.fprint('Proxies Banned - Rotating','red')
				self.proxy = Main.get_proxy(proxies)

			if response.url == 'https://www.supplystore.com.au/shop/checkout/submit.aspx':
				Main.fprint('Proccessing Payment...','yellow')

				soup = BeautifulSoup(response.content,'lxml')
				scripts = soup.find_all('script',attrs={'type':'text/javascript'})
				for i in scripts:
					if 'sharedPayment' in str(i):
						access = str(i).strip()

				access = access.split('eWAYConfig',1)[-1]
				access = access.split('};',1)[0]
				access = access.split('= {',1)[-1]
				access = access.replace('"','')
				access = access.replace("sharedPaymentUrl:",'')
				access = access.strip()
				Main.fprint('Successfully got checkout','green')
				self.access = str(access)
				return True
			else:
				Main.fprint('Failed proccessing payment','red')
				print(response.url)

	def get_token(self):
		try:
			response = requests.get('http://localhost:8080/fetch').content.decode('utf-8')
		except:
			Main.fprint('Unable to connect to captcha bank....','red')
			return False

		response = json.loads(response)

		for i in response:
			self.token = i['token']


class Sneakerboy:
	def __init__(self,tasks,taskid):

		self.config = Main.LoadJson('Sneakerboy','config.json')
		self.delay = int(self.config['delay'])

		self.session = requests.Session()
		print(tasks)
		self.profile = self.LoadProfiles()
		self.taskid = taskid


		self.price = None
		self.image = None
		self.title = None


		self.login_email = self.profile[tasks['PROFILE_NAME']]['Sneakerboy_Email']
		self.login_password = self.profile[tasks['PROFILE_NAME']]['Sneakerboy_Password']
		self.first_name = self.profile[tasks['PROFILE_NAME']]['FName']
		self.last_name = self.profile[tasks['PROFILE_NAME']]['LName']
		self.phone = self.profile[tasks['PROFILE_NAME']]['Phone']
		self.address = self.profile[tasks['PROFILE_NAME']]['Address']
		self.suburb = self.profile[tasks['PROFILE_NAME']]['Suburb']
		self.state = self.profile[tasks['PROFILE_NAME']]['State']
		self.postcode = self.profile[tasks['PROFILE_NAME']]['PCode']
		self.ccnum = self.profile[tasks['PROFILE_NAME']]['CCNum']
		self.expmonth = self.profile[tasks['PROFILE_NAME']]['CCExp'].split('/')[0]
		self.expyear = self.profile[tasks['PROFILE_NAME']]['CCExp'].split('/')[1]
		self.cvv = self.profile[tasks['PROFILE_NAME']]['CC_CVV']
		print(self.expmonth,self.expyear)



		
		self.sku = tasks['SKU']
		self.product = tasks['PRODUCT']
		self.size = tasks['SIZE']

		if self.login():
			t = time.time()
			if self.time_check():
				if self.sku_check():
					if self.cart_product():
						if self.shipping():
							if self.payment():
								l = time.time()
								self.speed = l - t
								if self.send_webhook(self.title,self.sku,self.size,'Sneakerboy FCFS',self.taskid,self.product,self.image):
									print('webhook sent.')
				else:
					self.sku = input('SKU Changed - Input a new sku: ')
					if self.cart_product():
						if self.shipping():
							if self.payment():
								l = time.time()
								self.speed = l - t
								if self.send_webhook(self.title,self.sku,self.size,'Sneakerboy FCFS',self.taskid,self.product,self.image):
									print('webhook sent.')
						
					else:
						pass


	def time_check(self):
		while True:
			return True
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			print(current_time)
			if current_time == '23:48:00':
				return True


	def send_webhook(self,title,sku,size,module,tasknum,product,image):
		config = Main.LoadJson('Sneakerboy','config.json')

		webhook = config['webhook']
		webhook = DiscordWebhook(url=str(webhook))
		embed = DiscordEmbed(title=str(title), description='SNKRLab CLI Checkout', color=242424,url=str(product))
		embed.add_embed_field(name='SKU',value=str(sku),inline=False)
		embed.add_embed_field(name='SIZE',value=str(size),inline=True)
		embed.add_embed_field(name='MODULE',value=str(module),inline=False)
		embed.set_author(name='Sneakerboy')
		# set footer
		embed.set_footer(text='SNKRLab CLI - Taking stock [{}] '.format(self.speed),icon_url='https://media.discordapp.net/attachments/782532739001614347/787653010142396446/SNKRLAB_21.png?width=333&height=333')

		# set timestamp (default is now)

		# add fields to embed
		embed.add_embed_field(name='Task', value=str(tasknum))
		embed.set_thumbnail(url=str(image))

		webhook.add_embed(embed)

		response = webhook.execute()
		return True
	def LoadProfiles(self):
		with open('Sneakerboy/profiles.csv','r') as csv_file:
				csv_reader = csv.reader(csv_file)
				next(csv_reader)
				profiles = {}

				for profile in csv_reader:
					try:
						profile_object = {
							'FName':profile[1],
							'LName':profile[2],
							'Email':profile[3],
							'Address':profile[4],
							'Suburb':profile[5],
							'State':profile[6],
							'PCode':profile[7],
							'Phone':profile[8],
							'CCNum':profile[9],
							'CCExp':profile[10],
							'CC_CVV':profile[11],
							'Sneakerboy_Email':profile[12],
							'Sneakerboy_Password':profile[13]
						}
						profiles[str(profile[0])] = profile_object

					except Exception as e:
						print(e)
						input('')

				return profiles	
	@classmethod
	def LoadTasks(self):
		with open('Sneakerboy/tasks.csv','r') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			tasks = {}
			task_num = 0


			for task in csv_reader:
				task_num += 1
				try:
					task_object = {
						'PROFILE_NAME':task[0],
						'SKU':task[1],
						'PRODUCT':task[3],
						'SIZE':task[2]
					}

					tasks[str(task_num)] = task_object
				except Exception as e:
					print(e)
					input('')

			return tasks

	def login(self):
		data = {
			'a':'login',
			'email':self.login_email,
			'password':self.login_password
		}

		print(data)
		logged_in = False

		while not logged_in:

			try:
				response = self.session.post('https://www.sneakerboy.com/includes/data_login.php',data=data)
			except Exception as e:
				print(e)
				Main.fprint('Proxies Banned - Rotating','red')

			if response.status_code == 200:
				try:
					responsejson = json.loads(response.content.decode('utf-8'))
				except Exception as e:
					print(e)
					Main.fprint('Failed to login [Fatal error]','red')
					time.sleep(self.delay)
					continue

				if 'You have been logged in' in str(responsejson['message']):
					Main.fprint(responsejson['message'],'green')
					time.sleep(self.delay)
					logged_in = True
					return logged_in
				else:
					Main.fprint(responsejson['message'],'red')
					time.sleep(self.delay)
					return False






			elif response.status_code != 200:
				Main.fprint('Unkown error [{}]'.format(str(response.status_code)))
	def sku_check(self):
		try:
			response = requests.get(self.product)
		except Exception as e:
			print(e)
			Main.fprint('Proxies Banned - Rotating','red')

		if response.status_code == 404:
			return False
		elif response.url != self.product:
			return False
		elif response.status_code == 200 and response.url == self.product:
			return True
	def cart_product(self):
		data = {
			'a':'add',
			'productstyle':self.sku,
			'sku':'{}-{}'.format(self.sku,self.size),
			'qty':'1',
			'site':'Sneakerboy'
		}

		carted = False
		while not carted:
			try:
				response = self.session.post('https://www.sneakerboy.com/includes/data_cart.php',data=data)
			except Exception as e:
				print(e)
				Main.fprint('Proxy Error','red')


			if response.status_code == 200:
				try:
					responsejson = json.loads(response.content.decode('utf-8'))

				except Exception as e:
					Main.fprint('failed to cart product [fatal error] - maybe out of stock','red')
					time.sleep(self.delay)

					continue

				if responsejson['status'] == 'success':
					Main.fprint('Product Carted','green')

					self.price = responsejson['data']['orderLines'][0]['unitValue']
					self.title = responsejson['data']['orderLines'][0]['title']
					self.image = responsejson['data']['orderLines'][0]['imageUrl']

					carted = True
					return carted
				else:
					Main.fprint('Product cart failed','red')
					print(responsejson['status'])
					time.sleep(self.delay)
					continue

			elif response.status_code != 200:
				Main.fprint('Unkown Error [{}]'.format(str(response.status_code)))
				time.sleep(self.delay)
				continue
	def shipping(self):
		data = {
	        'a': 'submit delivery and contacting you',
	        'a2': '',
	        'site': 'sneakerboy',
	        'voucher': '',
	        'deliveryoption': 'Deliver to You',
	        'name': str(self.first_name),
	        'surname': str(self.last_name),
	        'email': str(self.login_email),
	        'mobilephonecountrycode': 'AU',
	        'mobilephone': str(self.phone)
	    }
		ship = False


		while not ship:
		    try:
		    	response = self.session.post('https://www.sneakerboy.com/cart.php',data=data)
		    except Exception as e:
		    	print(e)
		    	Main.fprint('Proxies Failed','red')
		    	time.sleep(self.delay)
		    	continue

		    if response.status_code == 200:
		    	Main.fprint('Submitting Shipping...','yellow')
		    	ship = True
		    else:
		    	Main.fprint('failed to submit shipping','red')
		    	time.sleep(self.delay)
		    	continue

		ship_1 = False
		data = {
		    'a': 'submit shipping address',
		    'a2': '',
		    'site': 'sneakerboy',
		    'deliveryname': str(self.first_name),
		    'deliverysurname': str(self.last_name),
		    'deliveryaddress': '',
		    'deliveryaddress2': str(self.address),
		    'deliveryaddress3': '',
		    'deliverysuburb': str(self.suburb),
		    'deliverystate': str(self.state),
		    'deliverypostcode': str(self.postcode),
		    'deliverycountry': 'Australia',
		    'deliveryinstructions': '',
		    'copyaddress': 'Enter this Address as Billing Address'

		}
		while not ship_1:
			try:
				response = self.session.post('https://www.sneakerboy.com/cart.php',data=data)
			except Exception as e:
				print(e)
				Main.fprint('Proxies Failed','red')
				time.sleep(self.delay)
				continue

			if response.status_code == 200:
				Main.fprint('Proceeding to payment...','green')
				ship_1 = True
				return ship_1
			else:
				Main.fprint('Failed','red')
				time.sleep(self.delay)
				continue
	def payment(self):
		data = {
		    'a': 'submit order',
		    'a2': '',
		    'site': 'sneakerboy',
		    'voucher': '',
		    'paymentmethod': 'Pay by Credit Card',
		    'vpc_name': 'Bevan Shajan',
		    'vpc_CardNum': str(self.ccnum),
		    'vpc_CardSecurityCode': str(self.cvv),
		    'vpc_cardExp_month': str(self.expmonth),
		    'vpc_cardExp_year': '20'+str(self.expyear),
		    'staffassistedbycc': 'Web',
		    'staffassistedbycc': 'Web',
		    'staffassistedbycc': 'Web'
		}
		payment = False
		while not payment:
		    try:
		    	response = self.session.post('https://www.sneakerboy.com/cart.php',data=data)
		    except Exception as e:
		    	print(e)
		    	Main.fprint('Proxies Failed','red')
		    	time.sleep(self.delay)
		    	continue

		    if response.status_code == 200:
		    	Main.fprint('Successfuly Checked Out','green')
		    	payment = True
		    	return payment
		    else:
		    	Main.fprint('Failed to checkout','red')
		    	time.sleep(self.delay)
		    	continue






class Authentication:
	def __init__(self,api):
		self.api = api
		self.license = None
		self.hwid = self.setUUID

	@classmethod
	def setUUID(self):
		cmd = 'wmic csproduct get uuid'
		uuid = str(subprocess.check_output(cmd))
		pos1 = uuid.find("\\n")+2
		t = uuid[pos1:-15]
		return t

	def get_license(self):
	    headers = {
	        'Authorization': f'Bearer {self.api}'
	    }

	    req = requests.get(f'https://api.metalabs.io/v4/licenses/{self.license}', headers=headers)
	    if req.status_code == 200:
	        return req.json()
	    else:
	        return False

	def update_license(self):
	    headers = {
	        'Authorization': f'Bearer {self.api}',
	        'Content-Type': 'application/json'
	    }

	    payload = {
	        'metadata': {
	            'hwid': str(self.hwid)
	        }
	    }

	    req = requests.patch(f'https://api.metalabs.io/v4/licenses/{self.license}', headers=headers, json=payload)
	    if req.status_code == 200:
	        return True
	    else:
	        return False

	def load_j(self):
		with open('config.json') as e:
			file = json.load(e)
			return file
	def save_j(self,data):
		with open('config.json','w') as e:
			json.dump(data,e)
	def authenticate(self):
		authenticated = False
		while not authenticated:
			config = self.load_j()
			self.license = config['key']
			if self.license == 'None':
				key_input = input('Enter authentication key: ')
				self.license = str(key_input)
				license_data = self.get_license()
				if license_data:
					if license_data.get('metadata') != {}:
						if license_data.get('metadata')['hwid'] == str(self.hwid):
							print(colored('Successfuly authenticated','green'))
							key = self.load_j()
							key['key'] = self.license
							self.save_j(key)
							authenticated = True
						else:
							print(colored('Already active on another device','green'))
					else:
						self.license = str(key_input)
						status = self.update_license()
						if status:
							key = self.load_j()
							key['key'] = self.license
							self.save_j()

							print(colored('Successfully authenticated','green'))
							authenticated = True
				else:
					print(colored('Invalid License Key','red'))
					continue
			else:
				license_data = self.get_license()
				if license_data:
					if license_data.get('metadata') != {}:
						if license_data.get('metadata')['hwid'] == str(self.hwid):
							print(colored('Successfuly authenticated','green'))
							key = self.load_j()
							key['key'] = str(self.license)
			
							self.save_j(key)

							authenticated = True
						else:
							print(colored('Already active on another device','green'))
					else:
						status = self.update_license()
						if status:
							key = self.load_j()
							key['key'] = self.license
							self.save_j()

							print(colored('Successfully authenticated','green'))
							authenticated = True
				else:
					print(colored('Invalid License Key','red'))





					



class Start:
	def __init__(self):
		auth = Authentication('pk_dlsA8ck3dq57TQkKuMcPWrP02qNoDQbO')
		auth.authenticate()

		Main.clearconsole()


		with open('config.json','r') as e:
			key = json.load(e)
		now = datetime.now()

		style = style_from_dict({
		    Token.Separator: '#cc5454',
		    Token.QuestionMark: '#673ab7 bold',
		    Token.Selected: '#cc5454',  # default
		    Token.Pointer: '#673ab7 bold',
		    Token.Instruction: '',  # default
		    Token.Answer: '#f44336 bold',
		    Token.Question: '',
		})

		print(colored((figlet_format("SNKRLab CLI", font="standard")), "red"))
		print(colored('===========================================================','red'))
		print(colored('-----------------------','white'),colored('INFORMATION','red'),colored('-----------------------','white'))
		print(colored('===========================================================','red'))

		#-----------------------------
		print(colored('START TIME','red'),colored(': '+str(now.strftime("%a %H:%M:%S"))))
		print(colored('GROUP NAME','red'),colored(': SNKRLab AUSTRALIA'))
		print(colored('LICENSE','red'),colored(':'+str(key['key']),'white'),colored('[VALID]','green'))
		print(colored('===========================================================','red'))
		print(colored('-----------------------','white'),colored('MAIN MENU','red'),colored('-----------------------','white'))
		print(colored('===========================================================','red'))

		tasks = [{
				"type":"list",
				"name":"Operation",
				"message":"Operation:",
				"choices": ['FCFS','RAFFLE']
			}
		]

		answers = prompt(tasks,style=style)
		if answers['Operation'] == 'FCFS':
			module = [{
				"type":"list",
				"name":"Module",
				"message":"Module:",
				"choices":["Supplystore CC [Restock Mode]","Sneakerboy"]
			}]

		t = prompt(module,style=style)
		enable = [{
				"type":"list",
				"name":"Startz",
				"message":"Proceed:",
				"choices":["Start Tasks","Exit"]
		}]

		answers = prompt(enable,style=style)


		if answers['Startz'] == 'Start Tasks':
			Main.clearconsole()
			if t['Module'] == 'Supplystore CC [Restock Mode]':
				self.startSupplystore()
			if t['Module'] == 'Sneakerboy':
				self.startSneakerboy()




	def startSupplystore(self):
		tasks = Main.LoadTasks('Supplystore','tasks.csv')
		for i in tasks:
			t = Supplystore(tasks[i],i)

	def startSneakerboy(self):
		tasks = Sneakerboy.LoadTasks()
		for i in tasks:
			t = Thread(target=Sneakerboy,args=(tasks[i],i)).start()






#t = Sneakerboy(None)
t = Start()


