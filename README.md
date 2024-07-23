# gRPC_server_anomalib_MVTec
## Introduction
This is a gRPC server for anomalib using MVTec dataset.
## Tuturial
1. Put your torch model to "models\" folder
```
put your torch model to "models\" folder and run "_imageservice_server.py"
```
2. Install Anomalib and Torchvision
```
pip install requirements.txt
```
3. Open the server "image_server.py"
```
python image_server.py
``` 
- or
```
py image_server.py
```
4. Open the client "image_client.py"
```
python image_client.py
```
- or
```
py image_server.py
```
5. Test your image 
```
python image_client.py --image_path "test_image.png,test_image0.png"