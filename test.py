import json
from cryptography.fernet import Fernet # symmetric encryption



block={
    "satisfaction": "",
    "previous_block_id": "",
    "current_block_id": "",
    "timestamp" : "",
    "channel_id" : "",
    "sensor_val": "",
    "service_val": "",
    "runtime": ""
}

req_body={
	"time": "2021-07-07",
	"channel_id": "air_conditioner",
	"sensor_val": "23",
	"service_val": "26"
}

json_req = json.dumps(req_body)
dict_req = json.loads(json_req)

json_block = json_block = json.dumps(block)
dict_block = json.loads(json_block)







# 암복호화
class SimpleEnDecrypt:
    def __init__(self, key=None):
        if key is None:  # 키가 없다면
            key = Fernet.generate_key()  # 키를 생성한다
        self.key = key
        self.f = Fernet(self.key)

    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data)  # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8'))  # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data)  # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8'))  # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou




class Block():

    def __init__(self, index,timestamp, channel_id, sensor_val, service_val):
        self.index = index
        self.satisfaction = ""
        self.previous_block_id = ""
        self.current_block_id = self.calHash(timestamp, index)
        self.timestamp = timestamp
        self.channel_id = channel_id
        self.sensor_val = sensor_val
        self.service_val = service_val
        self.runtime = ""



    def calHash(self,timestamp, index):
        simpleEnDecrypt = SimpleEnDecrypt()
        message  = timestamp + str(index)
        return simpleEnDecrypt.encrypt(message)



class BlockChain:
    def __init__(self, ):
        self.chain = []
        self.difficulty = 5
        self.createGenesis()


    def createGenesis(self):
        self.chain.append(Block(0,"","","",""))


    def addBlock(self, nBlock):
        nBlock.previous_block_id = self.chain[len(self.chain)-1].current_block_id
        nBlock.current_block_id = nBlock.calHash(nBlock.timestamp, nBlock.index)
        self.chain.append(nBlock)



    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]


    def isValid(self):
        i = 1
        while(i<len(self.chain)):
            if(self.chain[i].current_block_id != self.chain[i].calHash()):
                return False
            if(self.chain[i].previous_block_id != self.chain[i-1].hash):
                return False

            i += 1
        return True



block = BlockChain()
block.addBlock(Block(len(block.chain),dict_req["time"],dict_req["channel_id"],dict_req["sensor_val"],dict_req["service_val"]))
block.addBlock(Block(len(block.chain),dict_req["time"],"hello",dict_req["sensor_val"],dict_req["service_val"]))
block.addBlock(Block(len(block.chain),dict_req["time"],"world",dict_req["sensor_val"],dict_req["service_val"]))
simpleEnDecrypt = SimpleEnDecrypt()



for block in block.chain:
    j_block = json.dumps(vars(block))
    dic_bloc = json.loads(j_block)
    if dic_bloc["channel_id"] == "air_conditioner":
        print(json.dumps(vars(block), indent=4))
    # print(json.dumps(vars(block), indent=4))







    # j_block = json.dumps(vars(block))
    # dic_bloc = json.loads(j_block)
    # if dic_bloc["channel_id"] == "air_conditioner":
    #     print(json.dumps(vars(block), indent=4))

