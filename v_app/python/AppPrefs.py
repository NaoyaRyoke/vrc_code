#
# @brief    Application Preferences class
#           アプリ環境設定クラス
#
import adam

class AppPrefs:

    # コンストラクタ
    def __init__(self):
        self.m_resolution = 0
        self.m_framerate_framenum = 0
        self.m_framerate_unittime = 0

        self.m_threshold = 0.0

        #クラウド送信用のパラメータ
        self.m_cloud_send_flag = False
        self.m_url = ""
        self.m_proxy_host = ""
        self.m_proxy_port = 0

    #
    # @brief    load Application Preferences function
    #           環境設定初期化関数
    #
    def load(self):
        print("load App Prefs")
        #設定値取得開始
        adam.lockAppPref()

        #画像の設定
        self.m_resolution = adam.getAppPref("Resolution")           # 解像度
        self.m_framerate_framenum = adam.getAppPref("Framerate_Framenum")      # フレームレート(フレーム数)
        self.m_framerate_unittime = adam.getAppPref("Framerate_Unittime")      # フレームレート(単位時間[sec])

        # 文字列で取得した小数をfloat型で持つ
        self.m_threshold = self.str_to_float(adam.getAppPref("Threshold"))             #信頼度の閾値

        #クラウド送信用のパラメータ
        self.m_cloud_send_flag = adam.getAppPref("CloudSendFlag")    #出力結果クラウド送信フラグ
        self.m_url = adam.getAppPref("URL")                          #送信先URL
        self.m_proxy_host = adam.getAppPref("proxyHost")             #送信先ホスト名
        self.m_proxy_port = adam.getAppPref("proxyPort")             #送信先ポート名

        #設定値取得完了
        adam.unlockAppPref()

    #
    # @brief    str to float function
    #           str型をfloat型に変換
    #
    def str_to_float(self, strValue):

        try:
            floatValue = float(strValue)
            return floatValue

        except ValueError as ex:        #例外処理
            print('QualityLevel Fomat Error')
            print(ex)

        except Exception as ex:        #例外処理
            print(ex)

