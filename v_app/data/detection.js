	console.log("start ...");

	var timer;

	var id;
	var tick;

	var canvas;
	var context;

	var screen_width;
	var screen_height;

	var colors = ["#DE6641", "#E8AC51", "#F2E55C", "#AAC863",
							  "#39A869", "#27ACA9", "#00AEE0", "#4784BF",
							  "#5D5099", "#A55B9A", "#DC669B", "#DD6673" ]

	var coloridx = -1;

	$(function() {

		//アプリインストール時の自動書き換えが行われていたら入力不可にする
		if ($("#id").val() != "12345678"){
			//id部を参照
			targetElement = document.getElementById('id');
			targetElement.disabled = true;
		}

		$("#startbutton").click(function(){
			//各パラメータをセット
			setParam();
	  	$("#startbutton").prop("disabled",true);
	  	$("#stopbutton").prop("disabled",false);
	  		startGetInfo();
			disp_init();
		});

		$("#stopbutton").click(function(){
			stopGetInfo();
	    $("#startbutton").prop("disabled",false);
	    $("#stopbutton").prop("disabled",true);
		});

	});

	//JSON取得を開始する
	function startGetInfo()
	{
		//JSONデータ取得
		getJson();
	}


	// *******************
	//  パラメータの設定
	// *******************
	function setParam()
	{
	  id = $("#id").val();
	  tick = $("#tick").val();

	  //初期値
	  screen_width=640;
	  screen_height=480;

	}

	// ***************************
	//  JSONデータ取得と表示
	// ***************************
	function getJson()
	{

		//Ajax通信
		$.ajax({
			type: "GET",
			url: "./adam.cgi",
			data: {	"methodName"	: "sendDataToAdamApplication",
							"installId"		: id,
							"processId"		: 0,
							"s_appDataType"	: 5000,
							"s_appData"		:""
			},
			success: dispInfo,
			error: function(res){
							}
		});

		//画像表示のチェックボックスの値を確認
		if($('#displayimage').prop('checked')){
			//画像取得
			getImg();
		}else{
			camera_img.src = "";
		}

		//指定時間後にもう一度自身を呼び出す
		timer = setTimeout("getJson()", tick);
	}

	// ***************************
	//	画像データの取得と表示
	// ***************************
	function getImg()
	{
		var request  = new XMLHttpRequest();

		// リクエストパラメータとURLの設定
		var param = "methodName=sendDataToAdamApplication&installId=" + id + "&s_appDataType=1&s_appData="
		var url = "./adam.cgi?" + param;

		request.open("GET", url, true);

		// blob形式で受信する
		request.responseType = "blob";

		request.onreadystatechange = function() {

			//受信正常時
			if (request.readyState == 4 && request.status == 200) {

	  			// 受信した画像データのblob URLを取得
				var blobUrl = URL.createObjectURL(request.response);

				// 画像表示
				camera_img.src = blobUrl;

				// 描画エリアサイズの更新
				if(screen_width != camera_img.width || screen_height != camera_img.height)
				{
				  	screen_width = camera_img.width;
				  	screen_height = camera_img.height;

				  	resize_screen();
				}

			}
		}

	  	request .send("");
	}

	// ***************************
	//	オブジェクト検出結果表示
	// ***************************
	function dispInfo(res)
	{
		console.log(res);

		//描画エリアクリア
		clearCanvas();

		//検出オブジェクトが存在している場合
		if( res.objectNum > 0 ){
			//初期化
			if(!disp_init){
				return;
			}

			//検出オブジェクトの数だけ繰り返し矩形描画
			for(var i = 0; i < res.objectNum; i++){
				var name = res.object[i].name;					//名前
				var baseX = res.object[i].square.baseX;			//矩形左上x座標
				var baseY = res.object[i].square.baseY;			//矩形左上y座標
				var width = res.object[i].square.width;			//矩形幅
				var height = res.object[i].square.height;		//矩形高さ

				drawSquare(baseX, baseY, width, height);

				//検出オブジェクトと一緒に注釈表示
				var score = res.object[i].score;
				var annotateText = name + " ("+ score+ ")";
				var annotateX =  baseX;
				var annotateY =  baseY;
				annotateObject(annotateText, annotateX, annotateY);

				//色の種類の上限に達したら
				if (colors.length === coloridx){
					//最初の色に戻る
					coloridx = -1;
				}
			}

			//表示用JSON文字列
			formated_json = JSON.stringify(res, null, "\t")
			//JSON文字列表示
			dispJsonData(formated_json);

		}

	}

	// *********
	//	初期化
	// *********
	function disp_init()
	{
		canvas = document.getElementById('disp');
		context = canvas.getContext('2d');

		// 画像表示領域（背景）を取得
		disp_parent = document.getElementById('disp_parent');
		disp_parent.style.background='#ffffff';

		// カメラ画像表示領域
		camera_img = document.getElementById('camera_img');

		//JSONデータ表示領域
		disp_json_area = document.getElementById('disp_json');

		resize_screen();

	}

	// *********************
	//	描画エリアリサイズ
	// *********************
	function resize_screen()
	{
		// 画像表示領域（背景）の更新
		disp_parent.style.width=screen_width;
		disp_parent.style.height=screen_height;

		// 描画エリア（カメラ画像＆検出表示canvas）設定の更新
		$('.relative').css('width', screen_width);
		$('.relative').css('height', screen_height);
		//描画機能が使えるブラウザであるかチェック
		if(canvas.getContext){

			//canvasタグの表示サイズを設定する
			$( 'canvas' ).get( 0 ).width  = screen_width;
			$( 'canvas' ).get( 0 ).height = screen_height;

			clearCanvas();
		}
		else
		{
			return 0;
		}
	}

	// **************
	//	矩形の描画
	// **************
	function drawSquare(baseX, baseY, width, height)
	{
		context.strokeStyle  = colors[++coloridx];			//矩形の色
		//矩形描画
		context.strokeRect(baseX, baseY, width, height);
	}


	// **************
	//	矩形の描画
	// *
	function drawPoint(x,y)
	{
		context.strokeStyle = '#e60033'
	}

	// *******************************************
	//	矩形の注釈描画（オブジェクト名と信頼度）
	// *******************************************
	function annotateObject(text, x, y)
	{
		//注釈の背景
		width = 100;	//幅
		height = 12;	//高さ
		context.fillStyle   = colors[coloridx];	//注釈背景の色
		//注釈背景描画
		context.fillRect(x, y, width, height);

		//注釈
		context.textAlign = "left";		//左詰め
		context.textBaseline = "top";	//描画基準は上部
		context.font = "9pt Arial";		//フォント
		context.fillStyle = '#000000';	//文字色
		//描画（第4引数はフォントの最大幅）
		context.fillText(text, x, y, 100);
	}

	//canvasエリアをクリアする
	function clearCanvas()
	{
		context.clearRect(0, 0, screen_width, screen_height);
		coloridx = -1;
	}

	//タイマーを解除する
	function stopGetInfo()
	{
	  if (timer) {
	    clearTimeout(timer);
	  }
	}

	//JSON文字列表示
	function dispJsonData(jsonData)
	{
		disp_json_area.textContent = jsonData;
	}
