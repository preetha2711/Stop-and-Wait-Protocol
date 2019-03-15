# Stop-and-Wait-Protocol

This project implements the stop-and-wait protocol using sockets and threading. The stop and wait protocol is a special case of the Go-back-N protocol , with window size = 1. Through this project we have illustrated and then tackled the possible errors that can happen through erroneous channels during stop-and-wait protocol communication.


The Stop-and-Wait protocol is a technique that is used to provide
reliability. In this protocol, one frame(in our case, on bit) is sent at a time. The sender does not send any more frames, until it receives an acknowledgement from the receiver for the same. If the acknowledgement fails to arrive within a given time frame, the sender then re-sends the entire frame. This condition is known as a timeout. On the receiver’s side, it sends an acknowledgement each time it receives a frame
