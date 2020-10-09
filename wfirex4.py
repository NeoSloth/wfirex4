import sys
import socket


# IPアドレス
ip = '192.168.1.100'
# ポート番号
port = 60001


# プロジェクター
projector_power = '582C050506050610060506050506050605050610061006050610061006100610051105060506050506100605060506050506051105110510060506100610061006100695'

# 切替機
selector = '592D0605050606050605060605060506050605110611051106100611061006110511060506050605060605060506060505060611051106100611051106110511051106FF92581606FFFFFFC8591606FFFFFFC8591605FFFFFFC9581705AA'

# リビング照明ON
light_living_on = '65310713061306130606060706120613061306070606061306130607060606070607050706130606060706060613060706130613050706130613061306060613060706FFBC641906A0'

# リビング照明OFF
light_living_off = '64320613061306130606060706130613061306060607061306130606060606070607061206130607061306060607060606130607060606130607061306130613060606FFBC641907D0'

# リビング照明 明るく
light_living_brightly = '65320612071306130606060706130613061306060607051306130607060606070607051306130607061207130606060706130606060706130507060705130613060706FFBC641906E3'

# リビング照明 暗く
light_living_darken = '65320612071207120706060607120712071207060606061306130607060606070606061306130613061306130606070606130606070606060607060606130613060706FFBC6419064A'



# WFIREX4からデータ取得
def get_wfirex():

  # WFIREX4から状態取得
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.sendall(b'\xAA\x00\x01\x18\x50')
    data = s.recv(1024)

  # 識別子チェック
  # int.from_bytes(data[:1], byteorder='big')
  # ペイロード長チェック
  # int.from_bytes(data[1:2], byteorder='big')
  # コマンドチェック
  # int.from_bytes(data[2:3], byteorder='big')
  # 安定度チェック
  # int.from_bytes(data[11:12], byteorder='big')
  # チェックサム
  # int.from_bytes(data[12:13], byteorder='big')

  # 湿度
  humi = int.from_bytes(data[5:7], byteorder='big') / 10
  # 温度
  temp = int.from_bytes(data[7:9], byteorder='big') / 10
  # 照度
  illu = int.from_bytes(data[9:11], byteorder='big')
  # 動作中
  acti = int.from_bytes(data[11:12], byteorder='big')

  return humi, temp, illu, acti


# FIREX4にデータ送信
def set_wfirex(wave_data_str, checksum=b''):

  # 赤外線波形データ
  wave_data = bytes.fromhex(wave_data_str) + checksum
  # 赤外線波形データ長(チェックサム分は「-1」する)
  wave_data_len = len(wave_data) - 1
  wave_data_len_hex = wave_data_len.to_bytes(2, 'big')

  # ペイロード
  payload = b'\x00' + wave_data_len_hex + wave_data
  # ペイロード長
  payload_len = len(payload).to_bytes(2, 'big')

  # ヘッダー
  header = b'\xAA' + payload_len + b'\x11'

  # ヘッダー　＋　ペイロード
  send_data = header + payload
  #print('送信データ：')
  #print(send_data.hex())

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.sendall(send_data)
    data = s.recv(1024)

  return data


# チェックサム調査
def searchChecksum(wave_data_str):

  for i in range(256):
    ret = set_wfirex(wave_data_str, checksum=i.to_bytes(1, 'big'))
    if len(ret) != 0:
      print('チェックサム：' + i.to_bytes(1, 'big').hex())
      break

  return ''


# WFIREX4からデータ取得

args = sys.argv
if len(args) == 1:
  sys.exit('引数がありません。')

# データ取得
if args[1] == 'get':
  humi , temp, illu, acti = get_wfirex()

  if args[2] == 'humi':
    #print("湿度：" + str(humi))
    sys.stdout.write(str(humi))

  elif args[2] == 'temp':
    #print("温度：" + str(temp))
    sys.stdout.write(str(temp))

  elif args[2] == 'illu':
    #print("照度：" + str(illu))
    sys.stdout.write(str(illu))

  elif args[2] == 'acti':
    #print("動作：" + str(acti))
    sys.stdout.write(str(acti))

  else:
    sys.exit('不明')

# チェックサム調査
elif args[1] == 'check':
  searchChecksum(args[2])

# プロジェクター
elif args[1] == 'projector_power':
  print('プロジェクター電源')
  ret = set_wfirex(projector_power)
  print('受信データ：')
  print(ret.hex())

# 切替機
elif args[1] == 'selector':
  print('切替機電源')
  ret = set_wfirex(selector)
  print('受信データ：')
  print(ret.hex())

# リビング照明ON
elif args[1] == 'light_living_on':
  print('リビング照明ON')
  ret = set_wfirex(light_living_on)
  print('受信データ：')
  print(ret.hex())

# リビング照明OFF
elif args[1] == 'light_living_off':
  print('リビング照明OFF')
  ret = set_wfirex(light_living_off)
  print('受信データ：')
  print(ret.hex())

# リビング照明 明るく
elif args[1] == 'light_living_brightly':
  print('リビング照明明るく')
  ret = set_wfirex(light_living_brightly)
  print('受信データ：')
  print(ret.hex())

# リビング照明 暗く
elif args[1] == 'light_living_darken':
  print('リビング照明暗く')
  ret = set_wfirex(light_living_darken)
  print('受信データ：')
  print(ret.hex())

# コマンド不明
else:
  sys.exit('不明')

# 正常終了
sys.exit()
