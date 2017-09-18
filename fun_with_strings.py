from flask import Flask, abort, jsonify, json, make_response, request, Response
from collections import Counter
import requests


class FunWithStringsAPI(object):
	__RandWordURL = 'http://setgetgo.com/randomword/get.php'
	__WikiExistPageURL = 'https://en.wikipedia.org/w/api.php?action=parse&page={}&prop=&format=json'
	__WikiPageURL = 'https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=extracts&exintro=&format=json'
	__RandJokeURL = 'http://api.icndb.com/jokes/random'
	__ConnectionErrorMsg = 'Connection error. Please check your network connection.'
	__NoPageErrorMsg = 'Ther''s no wiki page for this word. Please specify another one'
	__NoPageErrorCode = 432

	def __init__(self, name):
		self.app = Flask(name)
		self.app.add_url_rule('/', view_func=self.get_info, methods=['GET'])
		self.app.add_url_rule('/get_word', view_func=self.get_word, methods=['GET'])
		self.app.add_url_rule('/get_wiki', view_func=self.get_wiki, methods=['GET'])
		self.app.add_url_rule('/get_wiki/<word>', view_func=self.get_wiki, methods=['GET'])
		self.app.add_url_rule('/get_words/', view_func=self.get_words, methods=['GET'])
		self.app.add_url_rule('/get_words/<int:n>', view_func=self.get_words, methods=['GET'])
		self.app.add_url_rule('/get_words/<word>', view_func=self.get_words, methods=['GET'])
		self.app.add_url_rule('/get_words/<word>/<int:n>', view_func=self.get_words, methods=['GET'])
		self.app.add_url_rule('/get_joke', view_func=self.get_joke, methods=['GET'])

	def run(self):
		self.app.run(debug=True)

	def get_info(self):
		with open('readme.txt', 'r') as f:
			info = f.read()
			return make_response(jsonify(info), 200)

	def _get_word(self):
		resp = self.make_API_call(self.__RandWordURL)
		if resp.status_code != 200:
			return ''

		return resp.text

	def get_word(self):
		word = self._get_word()
		if word == '':
			return self.connection_error_resp()

		return make_response(word)
	
	def get_wiki(self, word=''):
		if word == '':
			word = self._get_word()
			if word == '':
				return self.connection_error_resp()

		exist_req = self.make_API_call(self.__WikiExistPageURL.format(word))

		#handle connection error
		if exist_req.status_code != 200:
			return self.connection_error_resp()

		if hasattr(exist_req, 'json'):
			exist_req = exist_req.json()

		if 'error' in exist_req:
			return make_response(jsonify(exist_req), self.__NoPageErrorCode)

		page_id = exist_req['parse']['pageid']
		resp = self.make_API_call(self.__WikiPageURL.format(word))
		if resp.status_code != 200:
			return resp

		try:
			text = resp.json()['query']['pages'][str(page_id)]['extract']
		except KeyError:
			resp = {"error": self.__NoPageErrorMsg}
			return make_response(jsonify(resp), 404)

		self.text = text
		self.word = word

		return make_response(jsonify({word: text}), 200)

	def count_words(self):
		self.text.replace('.', ' ')
		words = self.text.split()
		self.wordcount = Counter(words)

	def get_words(self, word='', n = 5):
		# if there's no preloaded text or user specify word explicitly - get a word
		if not hasattr(self, 'text') or word != '':
			resp = self.get_wiki(word)
			if resp.status_code == self.__NoPageErrorCode:
				resp = {"error": self.__NoPageErrorMsg}
				return make_response(jsonify(resp), 404)
			elif resp.status_code != 200:
				return self.connection_error_resp()

		self.count_words()

		sorted_list = sorted(self.wordcount, key=self.wordcount.get, reverse=True)
		if n > len(sorted_list):
			n = len(sorted_list)
		top = [(sorted_list[i], self.wordcount[sorted_list[i]]) for i in range(n)]

		return make_response(jsonify({self.word: top}), 200)

	def get_joke(self):
		first_name = request.args.get('firstName')
		last_name = request.args.get('lastName')
		param = {}
		if first_name is not None:
			param['firstName'] = first_name
		if last_name is not None:
			param['lastName'] = last_name

		resp = self.make_API_call(self.__RandJokeURL, param)
		resp = resp.json()

		if 'success' in resp['type']:
			return make_response(jsonify(resp['value']['joke']), 200)
		else:
			return self.connection_error_resp()

	def make_API_call(self, url = '', params = {}):
		try:
			resp = requests.get(url, params)
			return resp
		except requests.exceptions.ConnectionError:
			return self.connection_error_resp()

	def connection_error_resp(self):
		resp = {"error": self.__ConnectionErrorMsg}
		return make_response(jsonify(resp), 503)
	
if __name__ == '__main__':
	fs = FunWithStringsAPI(__name__)
	fs.run()
