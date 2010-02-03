from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from django.utils import simplejson
from gdata.spreadsheet import text_db


# The required Google account to access Google Spreadsheets
SPREADSHEET_USERNAME = '' # e.g. example@gmail.com
SPREADSHEET_PASSWORD = '' # e.g. password

# The optional API access key
ACCESS_KEY = '' # e.g. secret_key


class MainPage(webapp.RequestHandler):

	# Check whether var is None, '', or 0
	def _is_invalid(self, var):
		if var:
			return False
		self.response.set_status(400, 'Bad Request')
		return True

	# Check for the API key
	def _get_api_key(self):
		key = self.request.get('key')
		if ACCESS_KEY == '' or ACCESS_KEY == key:
			return False
		self.response.set_status(400, 'Bad Request' + key + 'xx')
		return True

	# Get the call parameters
	def _get_params(self):
		op = self.request.get('op')
		row = self.request.get('row')
		data = self.request.get('data')

		if self._is_invalid(op): return True, None, None, None
		try:
			if not self._is_invalid(data):
				data = simplejson.loads(data)
		except:
			return True, None, None, None

		return False, op, row, data

	# Get the necessary database name and table name
	def _get_db_and_table(self, db_name, table_name):
		client = memcache.get('client')
		if client is None:
			try:
				client = text_db.DatabaseClient(username=SPREADSHEET_USERNAME, password=SPREADSHEET_PASSWORD)
			except:
				return True, None, None
			memcache.set(key = 'client', value = client, time = 3600)

		db = memcache.get('db')
		if db is None:
			try:
				db = client.GetDatabases(name=db_name)
			except:
				return True, None, None
			if self._is_invalid(len(db)): return True, None, None
			memcache.set(key = 'db', value = db, time = 3600)

		table = memcache.get('table')
		if table is None:
			try:
				table = db[0].GetTables(name=table_name)
			except:
				return True, None, None
			if self._is_invalid(len(table)): return True, None, None
			memcache.set(key = 'table', value = table, time = 3600)

		return False, db[0], table[0]

	# Process HTTP GET calls
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'

		failed = self._get_api_key()
		if failed: return

		path = self.request.path.split('/')
		path = filter(None, path)

		if len(path) != 3:
			self.response.set_status(400, 'Bad Request')
			return

		db_name = path[0]
		table_name = path[1]
		row = path[2]

		failed, db, table = self._get_db_and_table(db_name, table_name)
		if failed: return

		if self._is_invalid(row): return
		record = table.GetRecord(row_number=row)
		if self._is_invalid(record): return
		try:
			output = simplejson.dumps(record.content)	
			self.response.out.write(output)
			self.response.set_status(200) # OK
		except:
			self.response.set_status(400, 'Bad Request')

	# Process HTTP POST calls
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'

		failed = self._get_api_key()
		if failed: return

		path = self.request.path.split('/')
		path = filter(None, path)

		if len(path) != 2:
			self.response.set_status(400, 'Bad Request')
			return

		db_name = path[0]
		table_name = path[1]

		failed, db, table = self._get_db_and_table(db_name, table_name)
		if failed: return

		failed, op, row, data = self._get_params()
		if failed: return

		if op == 'select':
			if self._is_invalid(row): return
			try:
				record = table.GetRecord(row_number=row)
				if self._is_invalid(record): return
				output = simplejson.dumps(record.content)	
				self.response.out.write(output)
			except:
				self.response.set_status(400, 'Bad Request')
				return

		elif op == 'update':
			if self._is_invalid(row): return
			if self._is_invalid(data): return
			try:
				record = table.GetRecord(row_number=row)
				if self._is_invalid(record): return
				for key, value in data.iteritems():
					record.content[key] = value
				record.Push()
			except:
				self.response.set_status(400, 'Bad Request')
				return

		elif op == 'insert':
			if self._is_invalid(data): return
			try:
				table.AddRecord(data)
			except:
				self.response.set_status(400, 'Bad Request')
				return

		elif op == 'delete':
			if self._is_invalid(row): return
			try:
				record = table.GetRecord(row_number=row)
				if self._is_invalid(record): return
				record.Delete()
			except:
				self.response.set_status(400, 'Bad Request')
				return

		else:
			self.response.set_status(400, 'Bad Request')
			return
			
		self.response.set_status(200) # OK



application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
