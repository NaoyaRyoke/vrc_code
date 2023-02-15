#
# @brief    Response class
#           レスポンスクラス
#

from FileControl import FileControl
from ConstDefine import ConstDefine

class Response:

    #
    # @brief    Create Response function
    #              レスポンスを組み立てて返す
    # @param response_file_path [in]     str            レスポンス形式のファイル名
    # @return                      Tuplee(str, bytes)    ヘッダ情報, ボディ情報
    def create_response_format(self, response_file_path):

        #ヘッダ情報取得
        header = self.get_header(response_file_path)

        # ファイル操作オブジェクト
        filecontrol = FileControl()
        # ボディ部設定
        body = filecontrol.get_file_data(response_file_path)

        return (header, body)




    #
    # @brief    Error Response function
    #              エラーレスポンス関数
    # @return                Tuplee(str, bytes)    ヘッダ情報, ボディ情報
    #
    def response_error(self):
        # HTTPレスポンスのボディ部をbytes型で作成
        body =     b"<HTML>\r\n"\
                    b"<HEAD></HEAD>\r\n"\
                    b"<BODY>\r\n"\
                        b"<H1>404 Not Found</H1>\r\n"\
                    b"</BODY>\r\n"\
                    b"The requested URL was not found on this server.\r\n"\
                b"</HTML>\r\n"

        # HTTPレスポンスのヘッダ部をstr型で作成
        header ="HTTP/1.1 404 Not Found\r\n"\
                "Content-Type: text/html; charset=iso-8859-1\r\n"

        return (header, body)



    #
    # @brief    get Header function
    #              ファイル名に対応したHTMLのヘッダ文字列を取得する
    # @param    filename [in]    str        ファイル名
    # @return                      str        ヘッダ情報
    def get_header(self, filename):

        #ファイル名の拡張子を探す
        posPeriod = filename.find(".")
        if -1 == posPeriod:
            return ConstDefine.OCTET_STREAM_HEADER

        #拡張子以降の文字列取得
        extension = filename[posPeriod:]

        if extension == ".html":
            return ConstDefine.HTML_HEADER

        if extension == ".js":
            return ConstDefine.JS_HEADER

        if extension == ".css":
            return ConstDefine.CSS_HEADER

        if extension == ".txt":
            return ConstDefine.TEXT_HEADER

        if extension == ".json":
            return ConstDefine.JSON_HEADER

        if extension == ".jpeg" or extension == ".jpg":
            return ConstDefine.JPEG_HEADER

        return ConstDefine.OCTET_STREAM_HEADER
