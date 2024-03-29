# DrinkWasteRcyleDetector

| Date | Paper                            |
| ---- | -------------------------------- |
| 2020-08-14 | [Drink Waste AI Documentation](https://drive.google.com/file/d/1AFDolgvZHiIeU5-q8bNTIMlSufdHFS8k/view?usp=drive_link) |

## Introduction

This project aims to leverage artificial intelligence (AI) to detect waste materials, with potential applications in recycling plants, as well as the development of waste-collecting devices and robots. The accompanying website serves as a demonstration of how this technology can be implemented effectively.
[Read More on ](https://drive.google.com/file/d/1AFDolgvZHiIeU5-q8bNTIMlSufdHFS8k/view?usp=drive_link)
## Technology Stack

- **Object Detection Model**: We employ YOLOv5, a powerful object detection model, to identify waste materials. If interested in the YOLO v5 model the repo is [here](https://github.com/ultralytics/yolov5). 
- **Dataset**: Our gratitude goes to Kaggle for providing access to the [Drinking Waste Classification dataset](https://www.kaggle.com/datasets/arkadiyhacks/drinking-waste-classification). This dataset includes contributions from Gary Thung and Mindy Yang, who manually collected portions of it. Their dedication to this task is greatly appreciated. You can find their repository [here](https://github.com/garythung/trashnet).
- **[Drink Waste AI Documentation](https://drive.google.com/file/d/1AFDolgvZHiIeU5-q8bNTIMlSufdHFS8k/view?usp=drive_link)**: For more information about how our system works, its performance, and its intended use and improvements, please refer to our school project paper in this [documentation](https://drive.google.com/file/d/1AFDolgvZHiIeU5-q8bNTIMlSufdHFS8k/view?usp=drive_link).
  
# Pages

#### Home Page

![Home Page](./static/img/home.png)

#### Result Page

### Result from Uploaded Photo

![Result from Uploaded Photo](./static/img/detection-result-uploaded-photo.png)

##### Result from Uploaded Video

![Result from Uploaded Video](./static/img/detection-result.png)

#### Camera Setup

![Camera Setup](./static/img/camera.png)

#### Upload Form

![Upload Form](./static/img/form.png)

## License

This project is licensed under the [MIT License](/LICENSE). Please review the [LICENSE.md](LICENSE) file for detailed licensing information.

## Contributing

We welcome contributions from the community. To contribute, follow these guidelines:

1. Fork the project repository.
2. Create a new branch for your contribution: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m "Add your feature"`.
4. Push your changes to your fork: `git push origin feature/your-feature-name`.
5. Open a pull request on the main repository with a clear description of your changes.

Kindly adhere to our [Code of Conduct](/CODE_OF_CONDUCT.md) when contributing.

By contributing to this project, you agree to license your contributions under the MIT License.
