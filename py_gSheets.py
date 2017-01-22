import httplib2
import os

import math
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class GBuffer:
	def __init__(self, width, height, sheetNames):
		credentials = self.__getCredentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
		self.__service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

		# Initialise a new Sheet document
		# TODO: properly support multi-target rendering. The start of this support is there where we
		#       create one sheet per target, but that's it - everywhere else assumes one RGBA target
		data = {}
		data['properties'] = {
			'title': 'Render [%s]' % time.ctime(),
			'defaultFormat': {
				'backgroundColor': {'red': 0.0, 'green': 1.0, 'blue': 0.0}
			}
		}
		data['sheets'] = []
		for sheetName in sheetNames:
			sheet = {'properties': {}}
			sheet['properties']['sheetId'] = 0
			sheet['properties']['title'] = sheetName
			sheet['properties']['gridProperties'] = {'rowCount': height, 'columnCount': width, 'hideGridlines': True}
			data['sheets'].append(sheet)
		res = self.__service.spreadsheets().create(body=data).execute()
		self.__spreadsheetId = res['spreadsheetId']
		self.__sheetId = res['sheets'][0]['properties']['sheetId']

		# Resize the cells to be tiny "squares"
		# (requesting 5x4 pixels seems to generate square results)
		data = {}
		data['requests'] = []
		data['requests'].append({
			'updateDimensionProperties': {
				'range': {
					'sheetId': self.__sheetId,
					'dimension': 'COLUMNS',
					'startIndex': 0,
					'endIndex': width
				},
				'properties': {
					'pixelSize': 4
				},
				'fields': 'pixelSize'
			}
		})
		data['requests'].append({
			'updateDimensionProperties': {
				'range': {
					'sheetId': self.__sheetId,
					'dimension': 'ROWS',
					'startIndex': 0,
					'endIndex': height
				},
				'properties': {
					'pixelSize': 5
				},
				'fields': 'pixelSize'
			}
		})
		self.__service.spreadsheets().batchUpdate(spreadsheetId=self.__spreadsheetId, body=data).execute()

	def __getCredentials(self):
		# THE BLOCK BELOW IS LIFTED FROM GOOGLE'S TUTORIAL
		# (https://developers.google.com/sheets/api/quickstart/python)
		SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
		CLIENT_SECRET_FILE = 'client_secret.json'
		APPLICATION_NAME = 'Google Sheets PRMan Display Driver'
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-d_gSheets.json')
		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			credentials = tools.run_flow(flow, store, None)
			print 'Storing credentials to ' + credential_path
		return credentials

	def updateCells(self, rowMin, rowMaxPlusOne, colMin, colMaxPlusOne, rgba):
		# Fill a buffer with (gamma-corrected) RGB data
		rgbaRows = []
		i = 0
		for row in range(rowMaxPlusOne-rowMin):
			rgbaRow = {'values': []}
			for col in range(colMaxPlusOne-colMin):
				rgbaData = {
					'userEnteredFormat': {
						'backgroundColor': {
							'red': math.pow(rgba[i][0], 1/2.2),
							'green': math.pow(rgba[i][1], 1/2.2),
							'blue': math.pow(rgba[i][2], 1/2.2)
						}
					}
				}
				i = i + 1
				rgbaRow['values'].append(rgbaData)
			rgbaRows.append(rgbaRow)

		# Update the background colour of the cells with the buffer
		data = {}
		data['requests'] = []
		data['requests'].append({
			'updateCells': {
				'range': {
					'sheetId': self.__sheetId,
					'startRowIndex': rowMin,
					'endRowIndex': rowMaxPlusOne,
					'startColumnIndex': colMin,
					'endColumnIndex': colMaxPlusOne
				},
				'rows': rgbaRows,
				'fields': 'userEnteredFormat.backgroundColor'
			}
		})
		self.__service.spreadsheets().batchUpdate(spreadsheetId=self.__spreadsheetId, body=data).execute()

