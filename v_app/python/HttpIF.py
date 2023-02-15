#
# @brief    HTTP Interface class
#           HTTP通信インターフェースクラス
#

from queue import Queue
import threading
import urllib
from urllib import request


class HttpIF(threading.Thread):

    #スレッドロック取得用
    _lock = threading.Lock()

    #コンストラクタ
    def __init__(self):
        threading.Thread.__init__(self)
        #キューオブジェクト
        self.m_que_object = Queue()

        #スレッド終了済みフラグ
        self.m_is_exit = False

        # mainのappPrefsオブジェクトを取得
        from __main__ import appprefs

        # 設定値をクラス変数にセット
        self.m_cloud_send_flag = appprefs.m_cloud_send_flag     #出力結果クラウド送信フラグ
        self.m_url = appprefs.m_url                             #送信先URL
        self.m_proxy_host = appprefs.m_proxy_host                #送信先ホスト名
        self.m_proxy_port = appprefs.m_proxy_port                #送信先ポート名

        print("[DEBUG]self m_cloud_send_flag:", self.m_cloud_send_flag)
        print("[DEBUG]self m_url:%s" % self.m_url)
        print("[DEBUG]self m_proxy_host:%s" % self.m_proxy_host)
        print("[DEBUG]self m_proxy_port:%s" % self.m_proxy_port)

        #プロキシ設定を行う
        self.setup_proxy()

        #ヘッダ設定
        self.m_headers = {"Content-Type" : "application/json"}

    #
    # @brief
    # クラウド送信フラグ取得
    # @return         [in] Boolean    クラウド送信フラグ
    #
    def get_cloud_send_flag(self):
        return self.m_cloud_send_flag
    #
    # @brief
    # スレッド終了フラグセット
    # @param exitflag        [in] Boolean    スレッド終了フラグ
    #
    def set_exit_flag(self, exitflag):
        self.m_is_exit = exitflag

    #
    #  @brief
    #  プロキシ設定
    #
    def setup_proxy(self):
        #プロキシ設定用
        proxies = {
            "http":"http://" + self.m_proxy_host + ":"+ str(self.m_proxy_port),
            "https":"https://" + self.m_proxy_host + ":"+ str(self.m_proxy_port)
        }
        proxy = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy)
        #OpenDirectorオブジェクトをインストール
        urllib.request.install_opener(opener)


    #
    #  @brief
    #  送信データ待ち受け開始
    #
    def run(self):

        #終了フラグを確認
        while not self.m_is_exit:
            #ロックを取得する
            with self._lock:

                #キューに要素が入っていたら
                if not self.m_que_object.empty():
                    #要素を取得
                    popData = self.m_que_object.get()
                    #タスクを実行
                    self.post_http(popData)
                    #タスクが完了したことをキューに伝える
                    self.m_que_object.task_done()

        print("\nFinish: self thread")



    #
    #  @brief send HTTP function
    #  HTTP送信関数
    #  @param json_data        [in] str    キューイングデータ
    #
    def post_http(self, json_data):

        # リクエスト組立
        request = urllib.request.Request(self.m_url,
                                         headers=self.m_headers,
                                         data=json_data.encode('utf-8'))
        try:
            #リクエスト送信
            with urllib.request.urlopen(request) as response:
                print("[DEBUG] RESPONSE STATUS CODE: ", response.getcode())

        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)

        except urllib.error.URLError as e:
            print(e.code)
            print(e.reason)

    #
    #  @brief queuing data function
    #  キューイング関数
    # @param q        [in] str    キューイングデータ
    #
    def put(self, q):

        # ロックを取得する
        with self._lock:
            #キューに要素を追加する
            self.m_que_object.put(q)

