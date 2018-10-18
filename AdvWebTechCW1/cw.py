import ConfigParser, json

from flask import Flask, render_template

app = Flask(__name__)

filename = "static/js/dictionary.json"

def getArtistNames(genre):
	with open(filename, 'r') as f:
		data = json.load(f)
	
		artistNameList = []

		for i in range(len(data['genre'])):
			if data['genre'][i]['name'] == genre:
				for j in range(len(data['genre'][i]['artist'])):
					artistNameList.append(data['genre'][i]['artist'][j]['name'])
	return artistNameList

def getArtistURLs(genre):
	with open(filename, 'r') as f:
		data = json.load(f)

		artistUrlList = []

		for i in range(len(data['genre'])):
			if data['genre'][i]['name'] == genre:
				for j in range(len(data['genre'][i]['artist'])):
					artistUrlList.append(data['genre'][i]['artist'][j]['artistURL'])
						
	return artistUrlList

def getAlbumNameList(name):
        with open(filename, 'r') as f:
                data = json.load(f)

                albumNameList = []

                for i in range(len(data['genre'])):
			 for j in range(len(data['genre'][i]['artist'])):
				if data['genre'][i]['artist'][j]['name'] == name:
					for k in range(len(data['genre'][i]['artist'][j]['albums'])):
						 albumNameList.append(data['genre'][i]['artist'][j]['albums'][k]['name'])

        return albumNameList

def getAlbumURLList(name):
        with open(filename, 'r') as f:
                data = json.load(f)

		albumUrlList = []

		for i in range(len(data['genre'])):
                         for j in range(len(data['genre'][i]['artist'])):
                                if data['genre'][i]['artist'][j]['name'] == name:
                                        for k in range(len(data['genre'][i]['artist'][j]['albums'])):
                                                 albumUrlList.append(data['genre'][i]['artist'][j]['albums'][k]['albumURL'])

        return albumUrlList

def getSongList(name):
	with open(filename, 'r') as f:
                data = json.load(f)

                songList = []

		for i in range(len(data['genre'])):
                         for j in range(len(data['genre'][i]['artist'])):
                                for k in range(len(data['genre'][i]['artist'][j]['albums'])):
					for l in range(len(data['genre'][i]['artist'][j]['albums'][k]['songs'])):
						if data['genre'][i]['artist'][j]['albums'][k]['name'] == name:
							songList.append(data['genre'][i]['artist'][j]['albums'][k]['songs'][l]['name'])
	return songList

def getLengthList(name):
        with open(filename, 'r') as f:
                data = json.load(f)

                lengthList = []
		
		for i in range(len(data['genre'])):
                         for j in range(len(data['genre'][i]['artist'])):
                                for k in range(len(data['genre'][i]['artist'][j]['albums'])):
                                        for l in range(len(data['genre'][i]['artist'][j]['albums'][k]['songs'])):
                                                if data['genre'][i]['artist'][j]['albums'][k]['name'] == name:
                                                        lengthList.append(data['genre'][i]['artist'][j]['albums'][k]['songs'][l]['length'])

	return lengthList

@app.route('/')
def root():
	return render_template('home.html'), 200

def init(app):
	config = ConfigParser.ConfigParser()
	try:
		config_location = "./etc/defaults.cfg"
		config.read(config_location)
		app.config['DEBUG'] = config.get("config", "debug")
		app.config['ip_address'] = config.get("config", "ip_address")
		app.config['port'] = config.get("config", "port")
		app.config['url'] = config.get("config", "url")
	except:
		print "Could not read configs from: ", config_location

@app.route('/explore')
def explore():
	with open(filename, 'r') as f:
		data = json.load(f)

		genres = []

		for i in range(len(data['genre'])):
			genres.append(data['genre'][i]['name'])

		genreURLs = []

		for i in range(len(data['genre'])):
                        genreURLs.append(data['genre'][i]['genreURL'])

	return render_template('explore.html', category="genre", catList=genres, catURL=genreURLs), 200

@app.route('/genre/<name>')
def getArtist(name):
	artists = []
	artistURLs = []

	artists = getArtistNames(name)
	artistURLs = getArtistURLs(name)

	print "/\/\/\/\/\/\/\/\/\/\/" + artistURLs[1]

	return render_template('explore.html', category="artist", catList=artists, catURL=artistURLs), 200

@app.route('/artist/<name>')
def getAlbum(name):
	albumNameList = []
	albumUrList = []
	albumNameList = getAlbumNameList(name)
        albumUrlList = getAlbumURLList(name)

	return render_template('explore.html', category="album", albumName=albumNameList, albumURL=albumUrlList)

@app.route('/album/<name>')
def getSongs(name):
        songList = []
        lengthList = []
	albumURL = ""

	with open(filename, 'r') as f:
		data = json.load(f)

		for i in range(len(data['genre'])):
        	                 for j in range(len(data['genre'][i]['artist'])):
                	         	for k in range(len(data['genre'][i]['artist'][j]['albums'])):
						if data['genre'][i]['artist'][j]['albums'][k]['name'] == name:
							albumURL = data['genre'][i]['artist'][j]['albums'][k]['albumURL']
							
        songList = getSongList(name)
        lengthList = getLengthList(name)
	return render_template('songs.html', url=albumURL, songNames=songList, songLength=lengthList, name=name)

@app.route('/allArtists')
def allArtists():
	with open(filename, 'r') as f:
                data = json.load(f)

                artistNameList = []

                for i in range(len(data['genre'])):
			for j in range(len(data['genre'][i]['artist'])):
        	                artistNameList.append(data['genre'][i]['artist'][j]['name'])

		artistUrlList = []

                for i in range(len(data['genre'])):
                	for j in range(len(data['genre'][i]['artist'])):
                        	artistUrlList.append(data['genre'][i]['artist'][j]['artistURL'])

	return render_template('explore.html', category="artist", catList=artistNameList, catURL=artistUrlList), 200

if __name__ == "__main__":
	init(app)
	app.run(
		host=app.config['ip_address'],
		port=int(app.config['port']))
