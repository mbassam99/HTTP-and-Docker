import json
import socketserver
import sys
import helper
from pymongo import MongoClient

client = MongoClient("mongo")
db = client["database"]
user = db["user"]
 

class MyTCPHandler(socketserver.BaseRequestHandler):


    def handle(self):

        nextID = 0

        received_data = self.request.recv(1024).strip()

        decodeData = received_data.decode("utf-8")
        checkData = str(decodeData).split()


        # DELETE STUFF
        if len(checkData) != 0 and checkData[0] == "DELETE" and checkData[1].__contains__("/users/") and len(checkData[1]) > 7:

            data_records = user.find({}, {"_id": 0})

            findInt = checkData[1].split()
            int_id = helper.find_int(findInt)

            dataFound = False

            for users in data_records:

                if users["id"] == int_id:
                    dataFound = True

                    user.delete_one({"id": int_id})

                    self.request.sendall(("HTTP/1.1 204 No Content\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n").encode())

            if dataFound:
                pass
            else:
                self.request.sendall(
                    "HTTP/1.1 404 Not Found\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 62\r\n\r\nno record for the requested id, or the record has been deleted".encode())

        # GET STUFFS
        elif len(checkData) != 0 and checkData[0] == "GET" and checkData[1].__contains__("/users/"):
            if len(checkData[1]) > 7:

                data_records = user.find({},{"_id": 0})

                findInt = checkData[1].split()

                int_id = helper.find_int(findInt)

                dataFound = True
                for users in data_records:
                    print("users: ", users)
                    print("int_id: ",int_id)
                    if users["id"] == int_id:
                        dataFound = True
                        data = users
                        byte_data = json.dumps(data)
                        self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length:" + str(
                        str(len(byte_data))) + "\r\nLocation: \r\n\r\n" + byte_data).encode())
                if dataFound:
                    pass
                else:
                    self.request.sendall(
                        "HTTP/1.1 404 Not Found\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nID NOT FOUND".encode())

        # GET USERS DATA STUFF
        elif len(checkData) != 0 and checkData[0] == "GET" and checkData[1] == "/users":

            data_records = user.find({},{"_id": 0})

            data = []

            for users in data_records:
                data.append(users)

            byte_records = json.dumps(data)

            self.request.sendall((
                "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length:" + str(len(byte_records)) + "\r\nLocation: \r\n\r\n" + byte_records).encode())

        # POST STUFFS
        elif len(checkData) != 0 and checkData[0] == "POST" and checkData[1].__contains__("/users"):

            getData = helper.find_username_email(decodeData)

            data_records = user.find({}, {"_id": 0})

            for users in data_records:
                nextID += 1

            dict = {"id": nextID, "email": str(getData[0]), "username": str(getData[1])}

            byte_dict = json.dumps(dict)

            user.insert_one(dict)

            self.request.sendall((
                "HTTP/1.1 201 Created\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length:" + str(len(byte_dict)) + "\r\nLocation: \r\n\r\n" + str(byte_dict)).encode())

        # UPDATE/PUT STUFF
        elif len(checkData) != 0 and checkData[0] == "PUT" and checkData[1].__contains__("/users/") and len(checkData[1]) > 7:

            data_records = user.find({},{"_id": 0})

            findInt = checkData[1].split()
            int_id = helper.find_int(findInt)

            dataFound = False

            for users in data_records:

                if users["id"] == int_id:

                    dataFound = True
                    previousData = users
                    getData = helper.find_username_email(decodeData)

                    dict = {"$set": {"id": int_id, "email": str(getData[0]), "username": str(getData[1])}}
                    user.update_one(previousData, dict)
                    byte_dict = json.dumps({"id": int_id, "email": str(getData[0]), "username": str(getData[1])})

                    self.request.sendall(("HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length:" + str(
                    str(len(byte_dict))) + "\r\nLocation: \r\n\r\n" + byte_dict).encode())

            if dataFound:
                pass
            else:
                self.request.sendall(
                    "HTTP/1.1 404 Not Found\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 62\r\n\r\nno record for the requested id, or the record has been deleted".encode())



        htmlFile = open("index.html", "r", encoding='utf-8').read().encode()
        js = open("functions.js", "r", encoding='utf-8').read().encode()
        css = open("style.css", "r", encoding='utf-8').read().encode()

        cat_image_file = open("image/cat.jpg", "rb")
        cat_byte_image = cat_image_file.read()
        cat_image_file.close()

        flamingo_image_file = open("image/flamingo.jpg", "rb").read()
        flamingo_byte_image = bytearray(flamingo_image_file)

        dog_image_file = open("image/dog.jpg", "rb").read()
        dog_byte_image = bytearray(dog_image_file)

        eagle_image_file = open("image/eagle.jpg", "rb").read()
        eagle_byte_image = bytearray(eagle_image_file)

        elephant_image_file = open("image/elephant.jpg", "rb").read()
        elephant_byte_image = bytearray(elephant_image_file)

        kitten_image_file = open("image/kitten.jpg", "rb").read()
        kitten_byte_image = bytearray(kitten_image_file)

        parrot_image_file = open("image/parrot.jpg", "rb").read()
        parrot_byte_image = bytearray(parrot_image_file)

        rabbit_image_file = open("image/rabbit.jpg", "rb").read()
        rabbit_byte_image = bytearray(rabbit_image_file)

        if len(checkData) != 0 and checkData[1] == "/":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " + str(
                                         len(htmlFile)) + "\r\nLocation: \javascript\r\n\r\n" + str(
                                         htmlFile.decode())).encode())

        elif len(checkData) != 0 and checkData[1] == "/functions.js":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/javascript; charset=utf-8\r\nContent-Length: " + str(
                                         len(js)) + "\r\nLocation: \css\r\n\r\n" + str(js.decode())).encode())

        elif len(checkData) != 0 and checkData[1] == "/style.css":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\nContent-Length: " + str(
                                         len(css)) + "\r\n\r\n" + str(css.decode())).encode())

        elif len(checkData) != 0 and checkData[1] == "/image/cat.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg\r\nContent-Length: " + str(
                                         len(cat_byte_image)) + "\r\n\r\n").encode() + cat_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/flamingo.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(flamingo_byte_image)) + "\r\n\r\n").encode() + flamingo_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/dog.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(dog_byte_image)) + "\r\n\r\n").encode() + dog_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/eagle.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(eagle_byte_image)) + "\r\n\r\n").encode() + eagle_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/elephant.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(elephant_byte_image)) + "\r\n\r\n").encode() + elephant_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/kitten.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(kitten_byte_image)) + "\r\n\r\n").encode() + kitten_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/parrot.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(parrot_byte_image)) + "\r\n\r\n").encode() + parrot_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/image/rabbit.jpg":

            self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: image/jpeg;\r\nContent-Length: " + str(
                                         len(rabbit_byte_image)) + "\r\n\r\n").encode() + rabbit_byte_image)

        elif len(checkData) != 0 and checkData[1] == "/hi":

            self.request.sendall(
                "HTTP/1.1 301 Moved Permanently\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 12\r\nLocation: \hello\r\n\r\nHello World!".encode())

        elif len(checkData) != 0 and checkData[1] == "/hello":

            self.request.sendall(
                "HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nHello World!".encode())

        else:
            self.request.sendall("HTTP/1.1 404 Not Found\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 9\r\n\r\nNot Found".encode())


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    server = socketserver.TCPServer((host, port), MyTCPHandler)
    server.serve_forever()
