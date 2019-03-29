import re, requests, os, shutil, math, sys, time, json
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

lock = Lock()

if len(sys.argv) < 5:
	print("Not enough arguments!")
	print(
"""
Usage:\tpython reddit-dl.py <type> <subreddit> <time_range> <limit> [min-likes]
  type:        One of (hot, new, rising, controversial, top).
               *Due to API limitations a maximum of 1000 top posts can be downloaded.
  subreddit:   The subreddit you want to download from.
  time_range:  One of (hour, day, week, month, year, all).
  limit:       Amount of posts to download.
""")
	quit()

type = sys.argv[1] # hot, new, rising, controversial, top
sub = sys.argv[2]
time_range = sys.argv[3]
limit = int(sys.argv[4])

image_links = []
images_downloaded = 0

os.makedirs('images/{}'.format(sub), exist_ok=True)

after = None

dots = 0

def get_page(_limit, _after):
	global dots
	sys.stdout.write("\rRequesting" + ('.' * dots))
	sys.stdout.flush()
	dots += 1
	url = "https://www.reddit.com/r/{}/{}.json?t={}&limit={}{}".format(sub, type, time_range, _limit, ("&after=" + _after if _after != None else ""))
	response = requests.get(url, headers = { 'User-agent': 'meme-dl.py' })
	sys.stdout.write('  ' + str(response.status_code))
	sys.stdout.flush()
	if response.status_code != 200:
		return
	obj = json.loads(response.text)
	for child in obj['data']['children']:
		image_links.append(child['data']['url'])
	global after
	after = obj['data']['after']

maxlen = 1

def update_download_progress(_name):
	global maxlen
	if len(_name) > maxlen:
		maxlen = len(_name)
	sys.stdout.write("\rDownloading images... [{}/{}] {}".format(images_downloaded, len(image_links), _name + (' ' * (maxlen - len(_name)))))
	sys.stdout.flush()

def download_image(_direct_link):
	if re.search(r'alb\.reddit\.com', _direct_link) != None:
		return False
	if re.search(r'https?', _direct_link) == None:
		_direct_link = "http:" + _direct_link
	response = requests.get(_direct_link, stream=True)
	if response.status_code != 200:
		print(response.status_code)
		return False
	srch = re.search(r'[A-Za-z0-9]+(\.jpg|\.png|\.jpeg|\.gif)', _direct_link)
	if srch == None:
		return False
	fname = srch.group()
	global images_downloaded
	ext = re.search(r'(jpg|png|jpeg|gif)', fname).group()
	lock.acquire()
	with open('images/{}/{}'.format(sub, str(images_downloaded) + '.' + ext), 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	images_downloaded += 1
	update_download_progress(fname)
	lock.release()
	return True

if limit <= 100:
	get_page(limit, None)
else:
	rlimit = int(limit / 100) * 100
	get_page(limit - rlimit, None)
	i = 0
	while i < rlimit / 100: # while i < [pages to get]
		get_page(100, after)
		i += 1

linkslen = len(image_links)

if(linkslen <= 100):
	print("\nStarting {} threads".format(len(image_links)))
	pool = ThreadPool(len(image_links))
	results = pool.map(download_image, image_links)
	pool.close()
	pool.join()
	del pool
else:
	print("\nStarting {} threads".format(linkslen))
	rlen = int(linkslen / 100) * 100
	if linkslen - rlen > 0:
		pool = ThreadPool(linkslen - rlen)
		pool.map(download_image, image_links[rlen:linkslen])
		pool.close()
		pool.join()
		del pool
	i = 0
	while i < rlen / 100:
		pool = ThreadPool(100)
		pool.map(download_image, image_links[i * 100:i * 100 + 100])
		pool.close()
		pool.join()
		del pool
		i += 1
	sys.stdout.write("\rDownloading images... [{}/{}]{}".format(images_downloaded, linkslen, ' ' * maxlen + ' '))

print("\nDone!")

# <img src="([^"])+" [^>]+ ?/?>

































