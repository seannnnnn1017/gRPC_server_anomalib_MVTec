from prediction import predict_image
from matplotlib import pyplot as plt
label,img=predict_image('prediction/models/model.pt', 'input_images/test_image0.png')
print(label)
plt.imshow(img)
plt.show()