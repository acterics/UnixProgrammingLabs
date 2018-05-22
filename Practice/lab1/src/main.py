from multiprocessing import Process, Pipe
import broker
import smoker
from generated.protobuf.components_pb2 import BrokerMessage


def f(name):
    print('hello {name}'.format(name=name))


if __name__ == '__main__':

    smoker1Receiver, smoker1Sender = Pipe()
    smoker2Receiver, smoker2Sender = Pipe()
    smoker3Receiver, smoker3Sender = Pipe()
    brokerReceiver, brokerSender = Pipe()

    smokerSenders = [smoker1Sender, smoker2Sender, smoker3Sender]

    brokerProcess = Process(target=broker.start, args=(
        smokerSenders, brokerReceiver))
    smoker1Process = Process(target=smoker.start, args=(
        BrokerMessage.TOBACCO, smoker1Receiver, brokerSender)
    )
    smoker2Process = Process(
        target=smoker.start, args=(
            BrokerMessage.PAPER, smoker2Receiver, brokerSender)
    )
    smoker3Process = Process(target=smoker.start, args=(
        BrokerMessage.MATCHES, smoker3Receiver, brokerSender)
    )

    brokerProcess.start()
    smoker1Process.start()
    smoker2Process.start()
    smoker3Process.start()

    brokerProcess.join()

    smoker3Process.join()
    smoker2Process.join()
    smoker1Process.join()
