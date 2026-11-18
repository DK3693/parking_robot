# Technical references

## Simulation and robotics middleware

- [NVIDIA Isaac Sim: ROS 2 Transform Trees and Odometry](https://docs.isaacsim.omniverse.nvidia.com/latest/ros2_tutorials/tutorial_series/tutorial_ros2_tf.html) — 모의 자세·속도·좌표계 연결.
- [NVIDIA Isaac Sim: ROS 2 Clock](https://docs.isaacsim.omniverse.nvidia.com/latest/ros2_tutorials/tutorial_series/tutorial_ros2_clock.html) — 시뮬레이션 시간과 센서 시각.
- [ROS REP 103](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst) — 단위와 축 방향.
- [ROS REP 105](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst) — 이동 로봇의 지도·주행·차체 좌표계.
- [PhysX documentation](https://nvidia-omniverse.github.io/PhysX/physx/5.1.0/_build/physx/latest/index.html) — 강체·접촉·마찰 모델의 기술 기반.

## Path-planning baseline

- [A Generic Trajectory Planning Method for Constrained All-Wheel-Steering Robots](https://arxiv.org/abs/2404.09677) — 조향 및 구동 제약을 고려한 궤적 계획의 기준 문헌.
- [AWSPlanning source repository](https://github.com/Rex-sys-hk/AWSPlanning) — C-AWS 탐색 코어 적용의 원본 구현. 프로젝트의 결합 형상·공통 명령 평가와 구분하여 활용했습니다.

## Perception and engineering tools

- [Ultralytics](https://github.com/ultralytics/ultralytics) — 카메라 차량 검출에 활용한 도구 계열.
- [AprilTag](https://github.com/AprilRobotics/apriltag) — 기준 표지 관측과 자세 보정 구성에 활용한 기술.
- [NumPy quantile](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html) — 분위수 기반 대표점 계산.

공개 저장소에는 프로젝트 설명, 익명화한 결과 데이터 및 범용 평가 도구를 수록합니다. 외부 라이브러리와 원본 알고리즘은 각 배포자의 라이선스와 출처를 따릅니다. 별도 재배포 라이선스는 부여하지 않습니다.
