import grpc
import imageservice_pb2
import imageservice_pb2_grpc
import argparse

def upload_image(stub, image_name):
    with open(image_name, 'rb') as f:
        image_data = f.read()
    request = imageservice_pb2.ImageUploadRequest(image_name=image_name, image_data=image_data)
    response = stub.UploadImage(request)
    print(response.message)

def download_image(stub, image_name, save_as):
    request = imageservice_pb2.ImageDownloadRequest(image_name=image_name)
    response = stub.DownloadImage(request)
    with open(save_as, 'wb') as f:
        f.write(response.image_data)
    print(f"Image downloaded and saved as {save_as}")
    
def predict_image(stub, image_name):
    
    if type(image_name) == str:
        request = imageservice_pb2.ImageDownloadRequest(image_name=image_name)
    else:
        request = imageservice_pb2.ImageDownloadRequest(image_names=image_name)
    response = stub.PredictImage(request)
    print(f"Prediction result: {response.prediction} ")
    for i, pred in enumerate(response.predictions):
        print(f"No.{i+1} Prediction:{pred}")

def run():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--image_paths', type=str, help='Comma-separated list of image paths')
    args = parser.parse_args()
    image_path = args.image_paths.split(',')
    print(image_path)
    options = [
        ('grpc.max_send_message_length', 100 * 1024 * 1024),  # 100 MB
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)  # 100 MB
    ]
    with grpc.insecure_channel('localhost:50051', options=options) as channel:
        stub = imageservice_pb2_grpc.ImageServiceStub(channel)
        #upload_image(stub, 'input_images/test_image.png')
        predict_image(stub, image_path)
        #predict_image(stub, ['input_images/test_image0.png', 'input_images/test_image.png'])
        #download_image(stub, 'output_images/output_segmentations.png', 'downloaded/downloaded_test_image.png')

if __name__ == "__main__":
    run()