from concurrent import futures
import grpc
import imageservice_pb2
import imageservice_pb2_grpc
from prediction import predict_image
from matplotlib import pyplot as plt
import time
import os

model_path='models\model.pt'

def check_files_in_directory(directory):
    # 列出資料夾內所有檔案和子資料夾的名稱
    items = os.listdir(directory)
    # 過濾出所有文件，忽略子資料夾
    files = [f"{directory}/{item}" for item in items if os.path.isfile(os.path.join(directory, item))]
    # 檢查文件列表是否為空
    if files:
        return files
    else:
        print("資料夾內沒有文件。")
        return False

    
class ImageService(imageservice_pb2_grpc.ImageServiceServicer):
    def UploadImage(self, request, context):
        image_name = request.image_name
        image_data = request.image_data
        with open(image_name, 'wb') as f:
            f.write(image_data)
        return imageservice_pb2.ImageUploadResponse(success=True, message="Image uploaded successfully")

    def PredictImage(self, request, context):
        time_stats = time.time()
        image_name = request.image_name
        print(f"2Predicting image {image_name}")
        if image_name: # string
            try:
                print('S1')
                img = plt.imread(image_name)
                prediction = predict_image(model_path=model_path,image_path=image_name)
                all_time=f"Prediction and transfer time: {time.time() - time_stats}"
                return imageservice_pb2.ImagePredictionResponse(prediction=f'{prediction}  {str(all_time)}')
            except:
                print('S2')
                folder=check_files_in_directory(image_name)
                
                if folder:
                    image_name=folder
                else:
                    context.abort(grpc.StatusCode.NOT_FOUND, "Image not found")
                    image_name = request.image_names
        image_name = list(image_name)


        print(f"Predicting multiple images {image_name}")
        predictions=[]
        for img_name in image_name: # list image paths
            try:
                print('M1')
                img = plt.imread(img_name)
                predictions.append(f'name: {img_name} '+predict_image(model_path=model_path,image_path=img_name))

            except:
                print('M2')
                folder=check_files_in_directory(image_name)
                
                if folder:
                    image_name=folder
                else:
                    image_name = request.image_names
                    context.abort(grpc.StatusCode.NOT_FOUND, f"path: {img_name} not found")

        
        all_time=f"Prediction and transfer time: {time.time() - time_stats}"
        predictions.append(all_time)
        return imageservice_pb2.ImagePredictionResponse(predictions=predictions)


    def DownloadImage(self, request, context):
        image_name = request.image_name
        try:
            with open(image_name, 'rb') as f:
                image_data = f.read()
            return imageservice_pb2.ImageDownloadResponse(image_data=image_data)
        except FileNotFoundError:
            context.abort(grpc.StatusCode.NOT_FOUND, "Image not found")

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 100 * 1024 * 1024),  # 100 MB
            ('grpc.max_receive_message_length', 100 * 1024 * 1024)  # 100 MB
        ]
    )
    imageservice_pb2_grpc.add_ImageServiceServicer_to_server(ImageService(), server)
    print('server start')
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()


