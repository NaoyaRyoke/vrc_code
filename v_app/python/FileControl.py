#
# @brief    File Control class
#           ファイル操作クラス
#

class FileControl:

    #
    # @brief    save file function
    #           ファイル保存関数
    # @param data                 [in] str    保存対象データ
    # @param path                 [in] str    データ保存先のパス
    #
    def save_file(self, data, path):
        #ファイル入出力関数
        try:
            #ファイルオープン（書き込みモード）
            fp = open(path, "w")

        except OSError as ex:            #例外処理
            print(ex)

        else:
            try:
                #保存対象データをファイルポインタへ書き込む
                fp.write(data)

            except Exception as ex:        #例外処理
                print(ex)

            finally:
            #ファイルクローズ
                fp.close()



    #
    # @brief    get file data function
    #           ファイル取得関数
    # @param path                 [in] str    データ保存先のパス
    # @return                          str    取得対象データ
    def get_file_data(self, path):

        try:
            #ファイルオープン
            fp = open(path, "rb")

        except OSError as ex:            #例外処理
            print(ex)

        else:
            try:
                #ファイルポインタをレスポンスのボディ部へ代入
                data = fp.read()

            except Exception as ex:        #例外処理
                print(ex)

            finally:
            #ファイルクローズ
                fp.close()

        return data



