from concurrent import futures
import grpc
import imageservice_pb2
import imageservice_pb2_grpc
from prediction import predict_image
from matplotlib import pyplot as plt
import time
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
        try:
            img = plt.imread(image_name)
            prediction = predict_image(model_path='prediction\models\model.pt',image_path=image_name)
            all_time=f"Prediction time: {time.time() - time_stats}"
            return imageservice_pb2.ImagePredictionResponse(prediction=f'{prediction}  {all_time}')
        except FileNotFoundError:
            context.abort(grpc.StatusCode.NOT_FOUND, "Image not found")

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
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()