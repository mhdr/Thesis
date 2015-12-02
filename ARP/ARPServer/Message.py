import json
import rsa
import binascii
import struct
import io
import pickle


class Message :
    def __init__(self,macs,uuid,signature):
        self.uuid=uuid

        self.macs=macs
        """:type: list"""

        self.signature=signature

    def to_json(self):
        instance= {"uuid": self.uuid, "macs": self.macs, "signature": self.signature}

        result=json.dumps(instance)
        return result

    def to_bin(self):
        length1=len(self.macs)
        length2=len(self.uuid)
        length3=len(self.signature)

        header=struct.pack("i",length1)+struct.pack("i",length2)+struct.pack("i",length3)
        payload=self.macs+self.uuid+self.signature

        result=header+payload

        return result

    def dumps(self):
        result= pickle.dumps(self)
        return result

    @staticmethod
    def loads(data):
        result=pickle.loads(data)
        return result

    @staticmethod
    def from_bin(dataB):
        reader=io.BytesIO(dataB)
        length1= reader.read(4)
        length2=reader.read(4)
        length3=reader.read(4)
        macs=reader.read(length1)
        uid=reader.read(length2)
        signature=reader.read(length3)
        reader.close()

        message=Message(macs,uid,signature)
        return message


    @staticmethod
    def from_json(j):
        instance=json.loads(j)

        uuid=instance["uuid"]
        macs=instance["macs"]
        signature=instance["signature"]

        message=Message(macs,uuid,signature)

        return message

    def verify(self):

        publicFile=open("public.pem")
        publicData=publicFile.read()
        publicFile.close()

        publicKey=rsa.PublicKey.load_pkcs1(publicData)

        m=Message.get_sum(self.macs,self.uuid)

        try:
            result=rsa.verify(m,self.signature,publicKey)
            return result
        except rsa.VerificationError:
            return False

    @staticmethod
    def get_sum(macs,uid):
        m=""

        for mac in macs:
            m=m+mac

        m=m+uid
        return m
