#image-augmentator
機械学習に用いる画像学習データの簡易複製ツール
（いわゆるdata augmentation用）

###開発環境＆使用ライブラリ
- python 3.5.1
- OpenCV3（画像処理部）
- PyQt5（GUI部）

※ Mac環境（macOSX El Capitan ver 10.11.6）で開発・動作確認

###ツール概要
指定したフォルダに格納されている画像に画像処理を施し複製する。

複製時に選択出来る画像より内容は以下のとおり。
- 上下・左右反転処理
- ノイズ付加処理
- フィルタリング処理（ぼけ）
- 色空間変換処理
- 回転処理

複製元となる画像は上書きされず、別名にて複製保存される。
（ファイル名は自動生成）
