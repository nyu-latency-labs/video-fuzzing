# Results

The benchmark_videos folder contains a set of videos of different types used to test how videos with different distribution of objects perform across models and analytics frameworks. The json files contain distribution of total number of objects and the object class on a frame level.

| Video name | Description | Duration (s) | FPS |
| --- | --- | --- | --- |
| video0 | Single frame of a car, repeated across the entire video | 40 | 25 |
| video1 | Composited video with normal distribution of car (μ=1, σ=0) | 40 | 25 |
| video2 | Composited video with normal distribution of car (μ=1, σ=1) | 40 | 25 |
| video3 | Composited video with normal distribution of car (μ=1, σ=0), person (μ=1, σ=1), motorbike (μ=1, σ=1) | 40 | 25 |

The result_res folder contains the raw detection data for each benchmarking run as a json so that data is available for future analysis.

## Benchmarks
When running the object detection, the first frame usually takes longer to execute as compared to the rest of the frames. So for each benchmark, the 2 graphs are plotted. The one on the left is with frame 1, and the one on the right without so that features can be seen more clearly.

### video0
#### Object Distribution:  
![Object Distribution](result_res/video0.png "video0")

#### Argus maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video0](result_res/argus_maskrcnn_video0_with_frame1.png "video0") | ![video0](result_res/argus_maskrcnn_video0_without_frame1.png "video0") |

Total expected detections: 1000  
Total actual detections: 2981  
Total hits: 1000  
Total misses: 0  
Precision: 33.545790003354576  
Recall: 100.0

#### Rocket maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video0](result_res/rocket_maskrcnn_video0_with_frame1.png "video0") | ![video0](result_res/rocket_maskrcnn_video0_without_frame1.png "video0") |

Total expected detections: 1000
Total actual detections: 999
Total hits: 999
Total misses: 0
Precision: 100.0
Recall: 99.9

#### Rocket framednntf:
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video0](result_res/rocket_framednntf_video0_with_frame1.png "video0") | ![video0](result_res/rocket_framednntf_video0_without_frame1.png "video0") |

Total expected detections: 1000  
Total actual detections: 0  
Total hits: 0  
Total misses: 999  
Precision: 0  
Recall: 0.0

#### Rocket ONNX Yolo: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video0](result_res/rocket_onnxyolo_video0_with_frame1.png "video0") | ![video0](result_res/rocket_onnxyolo_video0_without_frame1.png "video0") |

Total expected detections: 1000  
Total actual detections: 999  
Total hits: 999  
Total misses: 0  
Precision: 100.0  
Recall: 99.9

### video1
#### Object Distribution:  
![Object Distribution](result_res/video1.png "video1")


#### Argus maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video1](result_res/argus_maskrcnn_video1_with_frame1.png "video1") | ![video1](result_res/argus_maskrcnn_video1_without_frame1.png "video1") |

Total expected detections: 1000  
Total actual detections: 2081  
Total hits: 208  
Total misses: 792  
Precision: 9.995194617972128  
Recall: 20.8

#### Rocket maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video1](result_res/rocket_maskrcnn_video1_with_frame1.png "video1") | ![video1](result_res/rocket_maskrcnn_video1_without_frame1.png "video1") |

Total expected detections: 1000
Total actual detections: 969
Total hits: 969
Total misses: 30
Precision: 100.0
Recall: 96.9

#### Rocket framednntf: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video1](result_res/rocket_framednntf_video1_with_frame1.png "video1") | ![video1](result_res/rocket_framednntf_video1_without_frame1.png "video1") |

Total expected detections: 1000  
Total actual detections: 85  
Total hits: 64  
Total misses: 935  
Precision: 75.29411764705883  
Recall: 6.4

#### Rocket ONNX Yolo: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video1](result_res/rocket_onnxyolo_video1_with_frame1.png "video1") | ![video1](result_res/rocket_onnxyolo_video1_without_frame1.png "video1") |

Total expected detections: 1000  
Total actual detections: 126  
Total hits: 116  
Total misses: 883  
Precision: 92.06349206349206  
Recall: 11.6

### video2
#### Object Distribution:  
![Object Distribution](result_res/video2.png "video2")


#### Argus maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video2](result_res/argus_maskrcnn_video2_with_frame1.png "video2") | ![video2](result_res/argus_maskrcnn_video2_without_frame1.png "video2") |

Total expected detections: 300  
Total actual detections: 1136  
Total hits: 68  
Total misses: 232  
Precision: 5.985915492957746  
Recall: 22.666666666666668

#### Rocket maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video2](result_res/rocket_maskrcnn_video2_with_frame1.png "video2") | ![video2](result_res/rocket_maskrcnn_video2_without_frame1.png "video2") |

Total expected detections: 300
Total actual detections: 993
Total hits: 293
Total misses: 6
Precision: 29.506545820745217
Recall: 97.66666666666667

#### Rocket framednntf: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video2](result_res/rocket_framednntf_video2_with_frame1.png "video2") | ![video2](result_res/rocket_framednntf_video2_without_frame1.png "video2") |

Total expected detections: 300  
Total actual detections: 0  
Total hits: 0  
Total misses: 299  
Precision: 0  
Recall: 0.0

#### Rocket ONNX Yolo: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video2](result_res/rocket_onnxyolo_video2_with_frame1.png "video2") | ![video2](result_res/rocket_onnxyolo_video2_without_frame1.png "video2") |

Total expected detections: 300  
Total actual detections: 50  
Total hits: 50  
Total misses: 249   
Precision: 100.0  
Recall: 16.666666666666668

### video3
#### Object Distribution:  
![Object Distribution](result_res/video3.png "video3")


#### Argus maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video3](result_res/argus_maskrcnn_video3_with_frame1.png "video3") | ![video3](result_res/argus_maskrcnn_video3_without_frame1.png "video3") |

Total expected detections: 2450  
Total actual detections: 6450  
Total hits: 1207  
Total misses: 1243  
Precision: 18.713178294573645  
Recall: 49.265306122448976

#### Rocket maskrcnn: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video3](result_res/rocket_maskrcnn_video3_with_frame1.png "video3") | ![video3](result_res/rocket_maskrcnn_video3_without_frame1.png "video3") |

Total expected detections: 2450
Total actual detections: 1042
Total hits: 922
Total misses: 1526
Precision: 88.48368522072937
Recall: 37.63265306122449

#### Rocket framednntf: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video3](result_res/rocket_framednntf_video3_with_frame1.png "video3") | ![video3](result_res/rocket_framednntf_video3_without_frame1.png "video3") |

Total expected detections: 2450  
Total actual detections: 370  
Total hits: 275  
Total misses: 2173  
Precision: 74.32432432432432  
Recall: 11.224489795918368

#### Rocket ONNX Yolo: 
| With Frame 1 | Without Frame 1 |
| --- | --- | 
|![video3](result_res/rocket_onnxyolo_video3_with_frame1.png "video3") | ![video3](result_res/rocket_onnxyolo_video3_without_frame1.png "video3") |

Total expected detections: 2450  
Total actual detections: 1155  
Total hits: 557  
Total misses: 1891  
Precision: 48.22510822510822  
Recall: 22.73469387755102