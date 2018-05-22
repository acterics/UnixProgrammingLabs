import random
from generated.protobuf.components_pb2 import BrokerMessage


def start(smokersSenders, brokerReceiver):
    allComponents = [BrokerMessage.TOBACCO,
                     BrokerMessage.PAPER,
                     BrokerMessage.MATCHES]

    def sendToSmokers(message):
        for sender in smokersSenders:
            sender.send(message)

    def brokerPrint(text):
        print("Broker: {text}".format(text=text))
    brokerPrint('Broker started')

    while True:
        brokerMessage = BrokerMessage()
        brokerMessage.components.extend(random.sample(allComponents, 2))
        brokerPrint("Generated: \n{message}".format(message=brokerMessage))

        sendToSmokers(brokerMessage.SerializeToString())
        success = brokerReceiver.recv()
