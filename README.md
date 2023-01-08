# Autonomous-Car
Built a car in Carla that is able to drive autonomously within the simulated environment.

Technologies: Python, TensorFlow, Keras, and Carla.

Methodology: Developed and trained a Q-Learning Model in TensorFlow which controls the car's actions. This Q-Learning model was built upon 2 things:
1. The XCeption CNN model that was pre-trained using Keras & Reinforcement Learning.
2. A LIDAR image classification model that used snapshots taken of the given environment (snapshots from pre-installed LIDAR sensors on the car), so that the car emits pulsed laser light waves to be able to learn and classify nodes within its surroundings.

Accuracy: Achieved an accuracy of 87% based on the car's actions in the simulated scenarios.
