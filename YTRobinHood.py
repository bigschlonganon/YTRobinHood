from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
import pytube
import requests
import time
import os, glob
import os.path
from os import path

#Currently not used issues with session throws [ER1101] from requests
def site_login(options,user,password):
	driver = webdriver.Chrome(options=options)
	driver.get ("https://www.bitchute.com/")
	loginButton = driver.find_element_by_css_selector('.unauth-link a')
	loginButton.click()
	wait = WebDriverWait (driver, 10)
	wait.until(EC.visibility_of_element_located((By.ID,"id_username")))
	driver.find_element_by_id("id_username").send_keys(user)
	driver.find_element_by_id ("id_password").send_keys(password)
	driver.find_element_by_id("auth_submit").click()
	session_url = driver.command_executor._url  
	session_id = driver.session_id
	return session_url
	return session_id
	driver.quit()
	print("logged in")

def fileStructureInit():
	if not os.path.exists('downloads'):
		os.mkdir('downloads')
	if not os.path.exists("links.txt"):
		file = open("links.txt", "w") 
		
def cleanUp():
	dir = 'downloads'
	for file in os.scandir(dir):
		os.remove(file.path)			

def webdriverInit():
	options = webdriver.ChromeOptions() 
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument("--headless")
	return options

def writeLink(link):
	file = open("links.txt","a")
	file.write(str(link) + ';')
	print(link,"written to file")
	file.close()

def checkFile(link):
	with open("links.txt","r") as f:
		return link not in f.read().split(';')
		print("!!! Skipped",link," !!!")
		file.close()

def gatherLinks(options):
	driver = webdriver.Chrome(options=options)
	driver.get(baseurl)
	for link in driver.find_elements_by_tag_name('a'):
		if "watch?v=" in str(link.get_attribute('href')):
			links.append(link.get_attribute('href'))
	driver.quit()

def download(link):
	try:
		yt = YouTube(link)
		video = yt.streams.get_highest_resolution()
		print("__________________________________________")
		print()
		print(yt.title)
		print("downloading:.....")
		video.download('downloads',"video")
		videoID = link.split('watch?v=')[1]
		thumb = requests.get("https://img.youtube.com/vi/"+str(videoID)+"/maxresdefault.jpg").content
		with open('downloads/thumbnail.jpg', 'wb') as handler:
			handler.write(thumb)
		writeLink(link)
		print("download complete!")
		print("__________________________________________")
		return(yt)
	except pytube.exceptions.PytubeError as e:
		print("exception!!!!!!```")
		return None

def upload(yt,options,user,password):
	if yt != None:
		tries = 0
		submitTries = 0
		loginTries = 0
		driver = webdriver.Chrome(options=options)
		wait = WebDriverWait (driver, 20)
		uploadWait = WebDriverWait (driver, 300)
		while(loginTries <= 10):
			try:
				#Login code 
				driver.get ("https://www.bitchute.com/")
				loginButton = driver.find_element_by_css_selector('.unauth-link a')
				loginButton.click()
				wait.until(EC.visibility_of_element_located((By.ID,"id_username")))
				driver.find_element_by_id("id_username").send_keys(user)
				driver.find_element_by_id ("id_password").send_keys(password)
				driver.find_element_by_id("auth_submit").click()
				print("logged in!")
				#UPLOAD CODE
				wait.until(EC.visibility_of_element_located((By.ID,"userdropdown")))
				uploadButton = driver.find_element_by_xpath('//*[@id="nav-top-menu"]/div[2]/div[4]/a')
				uploadButton.click()
				wait.until(EC.visibility_of_element_located((By.ID,"upload_description")))
				driver.find_element_by_name("upload_title").send_keys(yt.title)
				break
			except TimeoutException as timeout:
				loginTries += 1
				print("trying again............")
				continue 
		try:
			if yt.description !=None:
				driver.find_element_by_name("upload_description").send_keys(yt.description)
		except WebDriverException as bmp:
				#change to strip BMP (emojis) out of yt.description
				driver.find_element_by_name("upload_description").send_keys("no description")
		while(tries <= 10):
			try:		
				#upload video and wait for progess to finish
				#!!! Find way to go to relative path
				driver.find_element_by_id("fileupload").send_keys("D:\\coding projects\\YTRobinHood\\downloads\\video.mp4")
				wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"progress")))
				print("Uploading video....")
				uploadWait.until(EC.invisibility_of_element_located((By.CLASS_NAME,"progress")))
				print("video uploaded!")
				#upload thumbnal and wait for progess to finish
				#!!! Find way to go to relative path
				driver.find_element_by_id("fileupload").send_keys("D:\\coding projects\\YTRobinHood\\downloads\\thumbnail.jpg")
				wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"progress")))
				print("Uploading thumbnail....")
				uploadWait.until(EC.invisibility_of_element_located((By.CLASS_NAME,"progress")))
				print("thumbnail uploaded!")
				
				while(submitTries <= 10):
					try:
						#click submit and wait for post request to be finalized
						#intecept exception happening here ???
						driver.find_element_by_id("finish-button").click()
						wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"channel-banner")))
						print()
						print("Video published!")
						break
					except ElementClickInterceptedException as timeout:
						submitTries += 1
						time.sleep(1)
						print("trying again............")
						continue
				break
			except TimeoutException as timeout:
				tries += 1
				print("trying again............")
				continue
		driver.quit()


user = "user"
password = "password"
#Make depended on input for scraping channels
#!!! Might require a .click() more button for channels

links =[]
fileStructureInit()

q1 = input("have you setup your login? Y | N: ")
if q1 == "N" or q1 == "n":
	user =input("enter your bitchute username or email: ")
	password = input("enter your bitchute password: ")
q2 = input("enter the youtube channel URL you want to use: ")
if "www.youtube.com/c/" in str(q2):
	baseurl = q2
	print("Gathering videos from: "+str(q2))
else:
	baseurl = "https://www.youtube.com/feed/trending"
	print("the url you entered is incorrect")
	print()
	print("starting scraper with youtube trending page close the CLI if you wish to try again")
	time.sleep(3)
	

while(1):
	links =[]
	gatherLinks(webdriverInit())
	for link in links: 
		if checkFile(link):
			yt = download(link)
			upload(yt,webdriverInit(),user,password)
			#to prevent file in use when cleaning up 
			time.sleep(2)
			cleanUp()
			yt = None