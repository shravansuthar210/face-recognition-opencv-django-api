from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
import json
import cv2
import base64
import numpy

new_count=1
# Create your views here.
def hy(request):
    return HttpResponse("FAce REcognitions api")


def face_detection(image_base64):
    image=cv2.imread(image_base64)
    grey_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    face_dectetor=cv2.CascadeClassifier("C:/Users/admin/Desktop/ml/cascad/haarcascade_frontalface_default.xml")
    faces=face_dectetor.detectMultiScale(grey_image,1.2,minNeighbors=8)
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),thickness=3)
    # new_count=new_count+1
    cv2.imwrite(str(1)+'.jpeg',image)
    return new_count,faces,grey_image

@api_view(['POST'])
def facedetecions(request):
    facedetecions_raw_data=JSONParser().parse(request)
    s=facedetecions_raw_data['image'][1:]
    
    # new_count=new_count+1

    new=base64.b64decode(bytes(s,'utf-8'))
    new_image=open(str(1)+".jpeg",'wb')
    new_image.write(new)
    new_image.close()

    face_detecto,face_detail ,imread=face_detection(str(1)+".jpeg")
    new_image_file=open('1.jpeg','rb')
    new_encode=base64.b64encode(new_image_file.read())
    new_image_file.close()

    return_data={
        "image":str(new_encode),
        "faces":str(face_detail)
    }
    return HttpResponse(json.dumps(return_data))

@api_view(['POST'])
def add_face(request):
    face_and_detail=JSONParser().parse(request)
    name=face_and_detail['name']
    i_file_open=open("identy.json",'r')
    try:
        json1=json.load(i_file_open)
    except Exception as e:
        print("Exception",e)
        json1={
            "data":[]
        }
    # data_list=json1['data']
    image=[]
    id_list=[]
    for i in json1['data']:
        if i['name']==name:
            face_number=i['face_number']
            break
    else:
        face_number=str(len(json1['data'])+1)
        json1["data"].append({"name":str(name),"face_number":face_number})
        file1=open("identy.json",'w')
        json.dump(json1,file1)
        # file1.write(json1)
        file1.close()

    face_detecto,face_detail ,imread=face_detection(str(1)+".jpeg")
    (x,y,w,h) = face_detail[0]
    face=imread[y:y+h,x:x+w]
    # img=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
    img=cv2.resize(face,(100,100))
    image.append(img)
    id_list.append(int(face_number))
    print(id_list)
    face_train(image,id_list)
    
    return HttpResponse(json.dumps({"status":"True"}))

def face_train(image,id_list):
    print(image,numpy.array(id_list))
    recognition=cv2.face.LBPHFaceRecognizer_create()
    try:
        recognition.read("model.h5")
    except Exception as e:
        print("Exception",e)
    recognition.train(image,numpy.array(id_list))
    recognition.write("model.h5")


@api_view(['POST'])
def face_name(request):
    facedetecions_raw_data=JSONParser().parse(request)
    s=facedetecions_raw_data['image'][1:]
    data={}
    face_detai=[]

    new=base64.b64decode(bytes(s,'utf-8'))
    new_image=open(str(1)+".jpeg",'wb')
    new_image.write(new)
    new_image.close()

    face_detecto,face_detail ,imread=face_detection(str(1)+".jpeg")
    model=cv2.face.LBPHFaceRecognizer_create()
    model.read("model.h5")
    for (x,y,w,h) in face_detail:
        face=imread[x:x+h,y:y+w]
        nbr,conf=model.predict(face)
        print(nbr,conf)
        if conf>0.5:
            i_file_open=open("identy.json",'r')
            json1=json.load(i_file_open)
            print(json1)
            for i in json1['data']:
                print(i)
                w=int(i['face_number'])
                print(w)
                if w==nbr:
                    name=i['name']
                    face_detail={"face_position":(x,y,w,h),"name":name}
                    face_detai.append(face_detail)
                    break

    new_image_file=open('1.jpeg','rb')
    new_encode=base64.b64encode(new_image_file.read())
    new_image_file.close()
    data['image']=str(new_encode)
    data['face_detai']=str(face_detai)

    return HttpResponse(json.dumps(data))
