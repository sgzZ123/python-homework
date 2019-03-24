# AppKey
AK = 'xbAeXztkLUyxQAs4qostCfTE'
# SecretKey
SK = 'YqnfSUQCE60iavabP3jPBmVFWaGygiMw'
# header
header = {'Content-Type	':'application/x-www-form-urlencoded'}
# 获取token的url地址
token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (AK,SK)
# 文字识别api地址
general_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
# 语种字典
language_dict = {'中英混合':'CHN_ENG',
                 '英文':'ENG',
                 '葡萄牙语':'POR',
                 '法语':'FRE',
                 '德语':'GER',
                 '意大利语':'ITA',
                 '西班牙语':'SPA',
                 '俄语':'RUS',
                 '日语':'JAP',
                 '韩语':'KOR'
                }
