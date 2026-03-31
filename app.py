from flask import Flask, request, render_template, jsonify
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import os
import requests
from dotenv import load_dotenv

load_dotenv()



class block(nn.Module):
    def __init__(self, in_channels, out_channels, identity_downsample=None, stride=1):
        super(block, self).__init__()
        self.expansion = 4
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels*self.expansion, kernel_size=1, stride=1, padding=0)
        self.bn3 = nn.BatchNorm2d(out_channels*self.expansion)
        self.relu = nn.ReLU()
        self.identity_downsample = identity_downsample
    def forward(self, x):
        identity = x; x = self.relu(self.bn1(self.conv1(x))); x = self.relu(self.bn2(self.conv2(x))); x = self.relu(self.bn3(self.conv3(x)));
        if self.identity_downsample is not None: identity = self.identity_downsample(identity)
        x = x + identity; x = self.relu(x); return x

class BrainCancerModelV1(nn.Module):
    def __init__(self, block, layers, image_channels, num_classes):
        super(BrainCancerModelV1, self).__init__()
        self.in_channels = 64; self.conv1 = nn.Conv2d(image_channels, 64, kernel_size=7, stride=2, padding=3); self.bn1 = nn.BatchNorm2d(64); self.relu = nn.ReLU(); self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, layers[0], out_channels=64, stride=1); self.layer2 = self._make_layer(block, layers[1], out_channels=128, stride=2); self.layer3 = self._make_layer(block, layers[2], out_channels=256, stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1)); self.fc = nn.Linear(256*4, num_classes)
    def forward(self, x):
        x = self.maxpool(self.relu(self.bn1(self.conv1(x)))); x = self.avgpool(self.layer3(self.layer2(self.layer1(x)))); x = x.reshape(x.shape[0], -1); return self.fc(x)
    def _make_layer(self, block, num_residual_blocks, out_channels, stride):
        identity_downsample = None; layers = []
        if stride != 1 or self.in_channels != out_channels*4:
            identity_downsample = nn.Sequential(nn.Conv2d(self.in_channels, out_channels*4, kernel_size=1, stride=stride), nn.BatchNorm2d(out_channels*4))
        layers.append(block(self.in_channels, out_channels, identity_downsample, stride)); self.in_channels = out_channels*4
        for i in range(num_residual_blocks - 1): layers.append(block(self.in_channels, out_channels))
        return nn.Sequential(*layers)

def BrainNet50(img_channels=3, num_classes=3):
    return BrainCancerModelV1(block, [1, 2, 3], img_channels, num_classes)



# Initialize the Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


device = "cuda" if torch.cuda.is_available() else "cpu"
model = BrainNet50(num_classes=3)
model.load_state_dict(torch.load("models/BrainCancerModel1_ver2.pth", map_location=device))
model.to(device)
model.eval()

class_names = ['brain_glioma', 'brain_menin', 'brain_tumor']
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def transform_image_and_predict(image_bytes):
    """Helper function to transform image and get prediction."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output_logits = model(img_tensor)
        output_probs = torch.softmax(output_logits, dim=1)
    
    pred_idx = torch.argmax(output_probs, dim=1).item()
    confidence = output_probs.max().item()
    predicted_class = class_names[pred_idx]
    
    return predicted_class, confidence

# Define the route for the home page
@app.route('/', methods=['GET'])
def home():
   
    return render_template('test.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        image_bytes = file.read()
        predicted_class, confidence = transform_image_and_predict(image_bytes)
        return jsonify({
            'prediction': predicted_class,
            'confidence': f"{confidence*100:.2f}%"
        })

@app.route('/gemini_summary', methods=['POST'])
def gemini_summary():
    data = request.json
    tumor_type = data.get('tumor_type')
    
    if not tumor_type:
        return jsonify({'error': 'No tumor type provided'}), 400
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    system_prompt = "You are a helpful medical assistant. You provide brief, easy-to-understand summaries for laypeople. Do not provide any medical advice. Respond only with the summary. Start your response with the tumor name as a title."
    user_query = f"Provide a brief, 2-3 sentence, easy-to-understand summary for a layperson about '{tumor_type}'. Focus on what it is, in general terms. IMPORTANT: Do not include any medical advice or treatment options."
    
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)