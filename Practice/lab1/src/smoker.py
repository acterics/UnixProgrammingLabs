import time
import random
from generated.protobuf.components_pb2 import BrokerMessage


def start(component, smokerReceiver, brokerSender):
    componentName = BrokerMessage.CigaretteType.Name(component)

    def smokerPrint(text):
        print("Smoker with {component}: {text}".format(
            component=componentName, text=text)
        )
    smokerPrint("Smoker started")

    while True:
        message = smokerReceiver.recv()
        brokerMessage = BrokerMessage()
        brokerMessage.ParseFromString(message)

        if component not in brokerMessage.components:
            sleepTime = random.randint(1, 5)
            smokerPrint("Received {c1} and {c2}. Start smoking {time}sec.".format(
                c1=BrokerMessage.CigaretteType.Name(
                    brokerMessage.components[0]),
                c2=BrokerMessage.CigaretteType.Name(
                    brokerMessage.components[1]),
                time=sleepTime
            ))
            time.sleep(sleepTime)
            brokerSender.send(True)
