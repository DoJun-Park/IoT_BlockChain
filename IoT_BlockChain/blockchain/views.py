from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cryptography.fernet import Fernet # symmetric encryption
from django.http import JsonResponse

import json


'''
req_body={
	"time": "2021-07-07",
	"channel_id": "air_conditioner",
	"sensor_val": "23",
	"service_val": "26"
}

block={
	"header": {
		"satisfaction": "",
		"previous_block_id": "",
		"current_block_id": "",
		"timestamp": ""
	},
	"data": {
		"channel_name": "",
		"sensor_val": "",
		"service_val": "",
		"runtime": ""
	}
}
'''

# 블록 id 암호화 기능
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





# 블록 class
class Block():
    def __init__(self, index,timestamp, channel_name, sensor_val, service_val):
        self.index = index
        self.satisfaction = ""
        self.previous_block_id = ""
        self.current_block_id = self.calHash(timestamp, index)
        self.timestamp = timestamp
        self.channel_name = channel_name
        self.sensor_val = sensor_val
        self.service_val = service_val
        self.runtime = ""


    def calHash(self,timestamp, index):
        simpleEnDecrypt = SimpleEnDecrypt()
        message  = timestamp + str(index)
        return simpleEnDecrypt.encrypt(message)



# 블록체인에서의 블록 생성
class BlockChain:
    def __init__(self):
        self.chain = []
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


class IoT_BlockChain_block(APIView):

    def post(self, request):
        global block

        body_unicode  = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        req_timestamp = body['time']
        req_channel_name = body['channel_name']
        req_sensor_val = body['sensor_val']
        req_service_val = body['service_val']


        block.addBlock(Block(len(block.chain),req_timestamp,req_channel_name,req_sensor_val,req_service_val))


        # 마지막 블록
        for recent_block in block.chain:
            continue
        

        blockJSONData = json.dumps(vars(recent_block))
        blockJSON = json.loads(blockJSONData)
        print(type(blockJSON))
        return JsonResponse(blockJSON, safe=False, status = 200)


    def get(self, request):
        # para로 받을 것    

        get_channel = request.GET.get('channel_name')
        send_block={}

        for find_block in block.chain:
            json_find_block = json.dumps(vars(find_block))
            dict_block = json.loads(json_find_block)
            if dict_block["channel_name"] == get_channel:
                send_block[dict_block["index"]]=dict_block
                # send_block.append(json.dumps(vars(find_block)))
        
        if len(send_block)==0:
            return Response("There is no block in this channel", status = 200)


  

        return JsonResponse(send_block, safe=False, status = 200)