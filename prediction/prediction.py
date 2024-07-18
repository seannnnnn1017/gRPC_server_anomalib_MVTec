from matplotlib import pyplot as plt
from anomalib.data.utils import read_image
from anomalib.deploy import TorchInferencer

def predict_image(model_path, image_path):

    image = read_image(path=image_path)  # 轉換為 RGB


    inferencer = TorchInferencer(
        path=model_path,
        device="auto"
    )
    image_name='output_images/output'
    print(image.shape)
    predictions = inferencer.predict(image=image)
    #print(predictions.pred_score, predictions.pred_label)  # predictions.pred_label
    # Visualize the raw anomaly maps predicted by the model.
    plt.imshow(predictions.anomaly_map)
    #plt.show()
    plt.imsave(f"{image_name}_anomaly_map.png", predictions.anomaly_map)  # 保存彩色圖像

    # Visualize the heatmaps, on which raw anomaly map is overlayed on the original image.
    plt.imshow(predictions.heat_map)
    #plt.show()
    plt.imsave(f"{image_name}_heat_map.png", predictions.heat_map)  # 保存彩色圖像

    # Visualize the segmentation mask.
    plt.imshow(predictions.pred_mask)
    #plt.show()
    plt.imsave(f"{image_name}_pred_mask.png", predictions.pred_mask)  # 保存彩色圖像

    # Visualize the segmentation mask with the original image.
    plt.imshow(predictions.segmentations)
    #plt.show()
    plt.imsave(f"{image_name}_segmentations.png", predictions.segmentations)  # 保存彩色圖像
    return f'{predictions.pred_label},{predictions.pred_score}'