import cv2
import requests
import json
import base64

# Function to capture an image
def capture_image(filename='image.jpg'):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press Space to Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite(filename, frame)
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to preprocess the image
def preprocess_image(filename='image.jpg'):
    image = cv2.imread(filename)
    # Example preprocessing: resizing the image
    resized_image = cv2.resize(image, (224, 224))
    cv2.imwrite('processed_image.jpg', resized_image)
    return 'processed_image.jpg'

# Function to call the GPT-4 Vision API
def analyze_image(image_path):
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    headers = {
        'Authorization': 'Bearer #Replace with API Key',  # Correctly format the API key
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image? Make your response as descriptive as possible."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    return response.json()

# Main function
def main():
    print("Capturing image...")
    capture_image()
    print("Preprocessing image...")
    processed_image_path = preprocess_image()
    print("Analyzing image with GPT-4 Vision API...")
    analysis_result = analyze_image(processed_image_path)
    print("Analysis Result:")
    print(json.dumps(analysis_result, indent=2))

if __name__ == "__main__":
    main()