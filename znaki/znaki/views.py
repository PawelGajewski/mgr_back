from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from PIL import ImageTk, Image
import zipfile
import numpy as np
from keras.models import load_model
from rest_framework import filters
import requests
import os
import jwt, datetime
import base64
from io import BytesIO
import pickle
from skimage.io import imread
from skimage.transform import resize
from rest_framework.permissions import IsAuthenticated
import xgboost
from sklearn import svm
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class SignsList(generics.ListCreateAPIView):
    queryset = Znak.objects.all()
    serializer_class = znakserializer
    name = 'znak'
    search_fields = ['name']
    ordering_fields = ['name']


class SignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Znak.objects.all()
    serializer_class = znakserializer
    name = 'znak-detail'


class SignSymbol(APIView):
    def post(self, request):
        znaki = Znak.objects.all()
        for znak in znaki:
            if znak.symbol == request.data['symbol']:
                this = znak
                serializer = znakserializer(this)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class Register(APIView):
    def post(self, request):
        serializer = userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class Auth(APIView):
    def post(self, request):
        token = request.data['jwt']
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = userserializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response



class Recognize(APIView):
    def post(self, request):
        usr = request.data['id']
        user = User.objects.filter(id=usr).first()
        classes = {
            1: 'b-33-20',
            2: 'b-33-30',
            3: 'b-33-50',
            4: 'b-33-60',
            5: 'b-33-70',
            6: 'b-33-80',
            7: 'b-34-80',
            8: 'b-33-100',
            9: 'b-33-120',
            10: 'b-25',
            11: 'b-26',
            12: 'a-6a',
            13: 'd-1',
            14: 'a-7',
            15: 'b-20',
            16: 'b-1',
            17: 'b-5',
            18: 'b-2',
            19: 'a-30',
            20: 'a-2',
            21: 'a-1',
            22: 'a-3',
            23: 'a-11',
            24: 'a-15',
            25: 'a-12b',
            26: 'a-14',
            27: 'a-29',
            28: 'a-16',
            29: 'a-17',
            30: 'a-24',
            31: 'a-32',
            32: 'a-18b',
            33: 'b-42',
            34: 'c-2',
            35: 'c-4',
            36: 'c-5',
            37: 'c-6',
            38: 'c-7',
            39: 'c-9',
            40: 'c-10',
            41: 'c-12',
            42: 'b-27',
            43: 'b-28'
        }
        Categories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                      '18',
                      '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
                      '35',
                      '36', '37', '38', '39', '40', '41', '42']
        res = str(request.data['file']).partition('.')[2]
        if res != 'zip':
            return Response("Wrong file type", status=status.HTTP_204_NO_CONTENT)
        imgzip = zipfile.ZipFile(request.data['file'])
        images = imgzip.infolist()
        prop_tab = []
        positive_recognitions = 0
        group = RecognitionGroup.objects.create(ownerID=user,
                                                label=request.data['label'],
                                                algorithm=request.data['algorithm'])
        group = RecognitionGroup.objects.last()
        indeks = 0
        for image in images:
            original_group = int(image.filename.split('_')[0])
            ifile = imgzip.open(image)
            img = Image.open(ifile)
            in_mem_file = BytesIO()
            img.save(in_mem_file, format="PNG")
            in_mem_file.seek(0)
            img_bytes = in_mem_file.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            pre = 'data:image/png;base64,' + base64_encoded_result_bytes.decode()
            data = {'file': pre,
                    'upload_preset': 'paoh74at'
                    }
            r = requests.post(url="https://api.Cloudinary.com/v1_1/ds9iegogh/image/upload", data=data)
            data = r.json()
            image = img.resize((30, 30))
            accuracy = 0
            if request.data['algorithm'] == 'Tensorflow':
                model = load_model(r'C:\\Users\\48513\Desktop\Programy\Python\zai\data\tensorflow_classifier.h5')
                image = np.expand_dims(image, axis=0)
                image = np.array(image)
                pred = np.argmax(model.predict(image), axis=-1)
                prop = model.predict(image)
                prop_tab.append(max(prop[0]))
                prop = max(prop[0])
                sign = classes[pred[0] + 1]
            if request.data['algorithm'] == 'SVM':
                model = pickle.load(open('data/svm_classifier_3.p', 'rb'))
                img = imread(data['url'])
                img_resize = resize(img, (30, 30, 3))
                l = [img_resize.flatten()]
                probability = model.predict_proba(l)
                sign = classes[int(Categories[model.predict(l)[0] + 1])]
                prop_tab.append(max(probability[0] * 100))
                prop = max(probability[0] * 100)
            if request.data['algorithm'] == 'XGBoost':
                print(indeks)
                indeks += 1
                model = pickle.load(open('data/xgb_model_10procent.p', 'rb'))
                img = imread(data['url'])
                img_resize = resize(img, (30, 30, 3))
                x = np.array(img_resize).reshape((1, -1))
                probability = model.predict_proba(x)
                sign = classes[int(Categories[model.predict(x)[0] + 1])]
                prop_tab.append(max(probability[0] * 100))
                prop = max(probability[0] * 100)
            #####################################################################
            rec = Recognition.objects.create(ownerID=user, image=data['url'], label=request.data['label'],
                                             predict=sign, probability=format(prop, '.4f'),
                                             algorithm=request.data['algorithm'], groupID=group,
                                             original_sign=classes[original_group + 1])
            if classes[original_group + 1] == sign:
                positive_recognitions += 1
        RecognitionGroup.objects.filter(pk=group.id).update(probability=format(sum(prop_tab) / len(prop_tab), '.4f'),
                                                            images_amount=len(prop_tab),
                                                            positive_recognized=positive_recognitions)
        if len(images) > 0:
            return Response("Completed", status=status.HTTP_200_OK)
        return Response("No data", status=status.HTTP_404_NOT_FOUND)


class RecognitionList(generics.ListAPIView):
    queryset = Recognition.objects.all()
    serializer_class = RecognitionSerializer
    # filter_backends = [filters.SearchFilter]
    filter_backends = [DjangoFilterBackend]
    # search_fields = ['=groupID__id', '=ownerID__id']
    filterset_fields = ['groupID__id', 'ownerID']


class RecognitioGroupList(generics.ListAPIView):
    queryset = RecognitionGroup.objects.all()
    serializer_class = RecognitionGroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=ownerID__id']


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = userserializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username']

