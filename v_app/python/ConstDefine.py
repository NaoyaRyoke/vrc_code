#
# @brief    Const Define class
#           定数定義クラス
#

import adam

class ConstDefine:
    HTML_FILE_PATH = adam.AppDataDirPath + "/detection.html"  #検出結果表示ページ
    JSON_FILE_PATH = adam.AppTmpDirPath + "/detection.json"   #jsonファイルの保存パス
    IMAGE_FILE_PATH = adam.AppTmpDirPath + "/detection.jpg"  # カメラからの画像保存パス

    TFLITE_FILE = adam.AppDataDirPath + "/gupa.tflite"             #学習済みモデル
    LABEL_LIST_FILE = adam.AppDataDirPath + "/gupalist.txt"          #オブジェクト名格納ファイル

    RESO_LIST = [(320,240),(640,480),(1280,720),(1920,1080)]        #解像度リスト


    # Response Header strings (HTML)
    HTML_HEADER ="Status: 200\r\n"\
                "Content-Type: text/html; charset=UTF-8\r\n"

    # Response Header strings (JavaScript)
    JS_HEADER = "Status: 200\r\n"\
                "Content-Type: application/javascript\r\n"

    # Response Header strings (CSS)
    CSS_HEADER ="Status: 200\r\n"\
                "Content-Type: text/css\r\n"

    # Response Header strings (Text)
    TEXT_HEADER ="Status: 200\r\n"\
                "Content-Type: text/plain;  charset=UTF-8\r\n"

    # Response Header jsons (JSON)
    JSON_HEADER = "Status: 200\r\n"\
                "Content-Type: application/json;  charset=UTF-8\r\n"


    # Response Header strings (JPEG)
    JPEG_HEADER ="Status: 200\r\n"\
            "X-Content-Type-Options: nosniff\r\n"\
            "Content-Type: image/jpeg\r\n"\
            "Cache-Control: no-cache\r\n"

    # Response Header strings (octet-stream)
    OCTET_STREAM_HEADER = "Status: 200\r\n"\
                        "Content-Type: application/octet-stream\r\n"


    DEFAULT_THRESHOLD = 0.5     #デフォルトの信頼度閾値
