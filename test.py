import gradio as gr
import grpc
import imageservice_pb2
import imageservice_pb2_grpc

def upload_and_predict_image(image_file):
    # 假設 gRPC 服務器已經在本地運行
    options = [
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ]
    channel = grpc.insecure_channel('192.168.1.117:50051', options=options)
    stub = imageservice_pb2_grpc.ImageServiceStub(channel)
    
    # 上傳圖片
    image_name = "uploaded_image.png"  # 指定一個檔案名稱用於上傳
    request = imageservice_pb2.ImageUploadRequest(image_name=image_name, image_data=image_file)
    stub.UploadImage(request)
    
    # 預測圖片
    request = imageservice_pb2.ImageDownloadRequest(image_name=image_name)
    response = stub.PredictImage(request)
    
    # 下載圖片並直接顯示
    save_as = f'downloaded/uploaded_image_segmentations.png'
    download_response = stub.DownloadImage(imageservice_pb2.ImageDownloadRequest(image_name='output_images/uploaded_image_segmentations.png'))
    with open(save_as, 'wb') as f:
        f.write(download_response.image_data)
    
    return response.prediction, save_as

iface = gr.Interface(
    fn=upload_and_predict_image,
    inputs=gr.File(label="Upload your image", type="binary"),
    outputs=[gr.Textbox(label="Prediction"), gr.Image(label="Predicted Image")],
    description="Upload an image to predict and view the predicted image directly."
)

iface.launch()
