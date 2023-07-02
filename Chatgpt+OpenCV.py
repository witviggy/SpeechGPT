import struct
import speech_recognition as sr
import openai
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
import cv2
import time

apikey = 'PASTE YOUR OPENAI API KEY HERE'
openai.api_key = apikey
model = 'text-davinci-003'
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set the speaking rate (words per minute)
engine.setProperty('volume', 1)  # Set the volume (float between 0 and 1)

wake_word = "elektra"
startup_sound = AudioSegment.from_file("startupsound.wav", format="wav")
r = sr.Recognizer()
mic = sr.Microphone()

classNames = []
classFile = "C:\\Users\\vigne\\PycharmProjects\\speechrecogn\\Object_Detection_Files\\Object_Detection_Files\\coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "C:\\Users\\vigne\\PycharmProjects\\speechrecogn\\Object_Detection_Files\\Object_Detection_Files\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath= "C:\\Users\\vigne\\PycharmProjects\\speechrecogn\\Object_Detection_Files\\Object_Detection_Files\\frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

start_time = time.time()
identified_objects = set()


def getObjects(img, thres, nms, draw=True, objects=[], min_confidence=0.6):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects and confidence >= min_confidence:
                objectInfo.append([className, confidence, box])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, className.upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return img, objectInfo


def wait_for_keyword():
    with mic as source:
        print("Waiting for the wake-word...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=7.0)
    try:
        text_input = r.recognize_google(audio)
        if wake_word in text_input.lower():
            return True
        else:
            return False
        print(f"User said: {text_input}")
        if "finish" in text_input.lower():  # End word
            play(startup_sound)
            print("Stopping the program...")
            exit()
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return False


count = 0
identified_objects = set()

while True:
    # Wake word
    while not wait_for_keyword():
        play(startup_sound)
        print("Word accepted Master!")
        break

    while True:
        # Recognize user input
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        last_print_time = time.time()

        counter = 0  # counter for number of object detections
        object_names = []  # list to store object names
        while True:
            success, img = cap.read()
            if not success:
                break
            if time.time() - start_time >= 5:
                result, object_list = getObjects(img, 0.45, 0.2, draw=True, min_confidence=0.6)
                for obj in object_list:
                    if obj[0] not in object_names:  # add new object to list
                        object_names.append(obj[0])
                        identified_objects.add(obj[0])
                        print(identified_objects)
                        counter += 1
                    if counter == 5:
                        break
                if counter == 5:
                    break
                if time.time() - start_time > 5:
                    distinct_objects = list(identified_objects)
                    text_input = ",".join(distinct_objects)
            else:
                result, _ = getObjects(img, 0.45, 0.2, draw=True, min_confidence=0.6)
                break
            cv2.imshow("Output", result)
            cv2.waitKey(1)
        if counter == 5:
            break

    #    while (count != 5):
    # Listen for user input
    print("I'm Ready Master!!!")
    count += 1
    # User input to OpenAI
    prompt = "give me a children story of 10 lines using" + text_input
    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=1000,
        temperature=0.9,
        n=1,
        stop=['---']
    )
    # Text to speech
    for result in response.choices:
        print(result.text)
        text = result.text
        engine.say(text)
        engine.runAndWait()
        wait_for_keyword()






