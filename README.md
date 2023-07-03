# SpeechGPT

The system utilizes the Raspberry Pi 4 Model B, a versatile single-board computer known for its computational power and connectivity options. The Raspberry Pi serves as the core hardware platform for running the project's software components.

The software relies on several libraries and models to achieve its functionality. The speech recognition functionality is implemented using the SpeechRecognition library, which provides a convenient interface to access speech recognition services like Google Speech Recognition. By capturing audio input from a microphone, the system waits for a specific wake word, such as "elektra," to initiate further actions.

Once the wake word is detected, the system starts capturing video frames using the OpenCV library. The captured frames are then processed using an object detection model based on the Single Shot MultiBox Detector (SSD) architecture. The SSD model, specifically the MobileNet V3 Large variant, is utilized for its efficient and accurate object detection capabilities.

The object detection model is loaded using pre-trained weights and configuration files. The COCO dataset's class names file is used to map the class IDs predicted by the model to human-readable labels. This allows the system to identify and label objects of interest in the captured frames.

The identified objects are stored in a set to ensure uniqueness and to keep track of all the objects encountered during the session. After a specified duration, the system generates a list of distinct objects and sends it as input to the OpenAI language model.

OpenAI's text generation model, specifically the Text Davinci 003 model, is employed to generate descriptive text based on the given input. The model is queried with a prompt that instructs it to create a children's story of 10 lines using the identified objects as inspiration. The generated text is then converted to speech using the pyttsx3 library and played back to the user through a speaker or headphones.

The project's architecture showcases the integration of different AI technologies, enabling a voice-controlled object detection system with interactive audio feedback. The speech recognition component enables hands-free control, allowing users to initiate actions by simply speaking the wake word. The object detection component leverages the power of computer vision to identify objects in real-time, which opens up possibilities for various applications such as smart surveillance, robotics, and augmented reality.

Furthermore, the integration with OpenAI's language model adds a creative aspect to the system. By generating stories based on the identified objects, the system fosters imagination and storytelling, making it an engaging tool for children and users of all ages.

In conclusion, the Raspberry Pi-based project demonstrates the fusion of speech recognition, object detection, and natural language processing technologies. It showcases the potential of combining these AI capabilities to create interactive and intelligent systems. With its voice-controlled object detection and story generation features, the project offers a glimpse into the exciting possibilities of AI integration in everyday life.

ALL THE BEST!!!
