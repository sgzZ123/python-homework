AK = 'xbAeXztkLUyxQAs4qostCfTE'
SK = 'YqnfSUQCE60iavabP3jPBmVFWaGygiMw'
header = {'Content-Type	':'application/x-www-form-urlencoded'}
token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (AK,SK)
general_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
