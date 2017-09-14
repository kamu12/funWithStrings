from flask import Flask, abort, jsonify, json, make_response
import requests


class FunWithStringsAPI(object):

	def __init__(self, name):
		self.app = Flask(name)
		self.app.add_url_rule('/get_word', view_func=self.get_word, methods=['GET'])
		self.app.add_url_rule('/get_wiki', view_func=self.get_wiki, methods=['GET'])
		self.app.add_url_rule('/get_words/', view_func=self.get_words, methods=['GET'])
		self.app.add_url_rule('/get_words/<int:n>', view_func=self.get_words, methods=['GET'])

	def run(self):
		self.app.run(debug=True)

	def get_word(self):
		resp = self.make_API_call('http://setgetgo.com/randomword/get.php')
		if resp.status_code != 200:
			return resp

		self.word = resp.text
		return make_response(self.word)
	
	def get_wiki(self):
		if not hasattr(self, 'word'):
			resp = self.get_word()
			if resp.status_code != 200:
				return self.connection_error_resp()

		existReq = self.make_API_call('https://en.wikipedia.org/w/api.php?action=parse&page='+
			self.word + '&prop=&format=json')

		#handle connection error
		if hasattr(existReq, 'json'):
			existReq = existReq.json()

		if 'error' in existReq:
			#if ther's no wiki page for current word, we could generate a new word interanlly
			#self.get_word()
			return make_response(jsonify(existReq), 432)
			
		pageId = existReq['parse']['pageid']
		resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&'+
			'titles=' + self.word + '&prop=extracts&exintro=&format=json')

		text = resp.json().get('query').get('pages').get(str(pageId)).get('extract')
		self.text = text

		return make_response(jsonify({self.word: self.text}), 200)

	def count_words(self):
		self.text.replace('.', ' ').replace('/n', '')
		words = self.text.split()
		self.wordcount = {}
		for word in self.text.split():
			if word not in self.wordcount:
				self.wordcount[word] = 1
			else:
				self.wordcount[word] += 1

	def get_words(self, n = 5):
		if not hasattr(self, 'text'):
			resp = self.get_wiki()
			if resp.status_code == 432:
				resp = {"error": "Ther's no wiki page for current word. Please generate other word"}
				return make_response(jsonify(resp), 404)
			elif resp.status_code != 200:
				return self.connection_error_resp()

		self.count_words()

		sortedList = sorted(self.wordcount, key=self.wordcount.get, reverse=True)
		if n > len(sortedList):
			n = len(sortedList)
		top = [(sortedList[i], self.wordcount[sortedList[i]]) for i in range(n)]

		return make_response(jsonify({self.word: top}), 200)

	def make_API_call(self, url = '', params = {}):
		try:
			resp = requests.get(url, params)
			return resp
		except requests.exceptions.ConnectionError:
			return self.connection_error_resp()

	def connection_error_resp(self):
		resp = {"error": "Connection error. Please check your network connection."}
		return make_response(jsonify(resp), 404)
	
if __name__ == '__main__':
	fs = FunWithStringsAPI(__name__)
	fs.run()
