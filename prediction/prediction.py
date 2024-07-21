from matplotlib import pyplot as plt
from anomalib.data.utils import read_image
from anomalib.deploy import TorchInferencer
import time
def predict_image(model_path, image_path):
    image = read_image(path=image_path)  # 轉換為 RGB

    inferencer = TorchInferencer(
        path=model_path,
        device="auto"
    )
    # 判斷是否有 device 屬性
    if hasattr(inferencer.model, 'parameters'):
        first_param = next(inferencer.model.parameters())
        device = first_param.device
        print(f"Using device: {device}")
    else:
        print("Cannot determine the device.")

    image_name = 'output_images/'+image_path.split('/')[-1].split('.')[0]
    print(image.shape)
    predictions = inferencer.predict(image=image)
    print(f'Label: {predictions.pred_label}, Score: {predictions.pred_score}')

    # 以下部分是保存和顯示圖像的代碼，如原先那樣處理

    plt.imsave(f"{image_name}_anomaly_map.png", predictions.anomaly_map)
    plt.imsave(f"{image_name}_heat_map.png", predictions.heat_map)
    plt.imsave(f"{image_name}_pred_mask.png", predictions.pred_mask)
    plt.imsave(f"{image_name}_segmentations.png", predictions.segmentations)

    return f'{predictions.pred_label},{predictions.pred_score}'
