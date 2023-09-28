from concurrent import futures
import logging
import random
import grpc
import missile_attack_pb2
import missile_attack_pb2_grpc


class Attack(missile_attack_pb2_grpc.AttackServicer):
    #getting missile info
    def assign(self, request, context):
        response = missile_attack_pb2.Response(
            x=random.randint(0,request.M-1),
            y=random.randint(0,request.M-1),
            radius=random.randint(1,4),
        )
        return response

def run_server():
    port="50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    missile_attack_pb2_grpc.add_AttackServicer_to_server(Attack(), server)
    server.add_insecure_port('192.168.28.247:50051')
    server.start()
    print("Server started listening on"+port)
    server.wait_for_termination()

#starting server
if __name__ == '__main__':
    run_server()
