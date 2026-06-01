# ROS 2 De Facto Tooling

Use this reference when a ROS 2 task needs tool selection, validation planning, or routing across common robotics stacks. Check the target ROS 2 distribution's official docs, package docs, and package index before assuming a tool is released or stable for that distro.

## Core Workspace

- `colcon`: default workspace build and test tool for ROS 2 packages.
- `rosdep`: resolves system dependencies from package metadata.
- `ament_cmake`: common build system for C++ and mixed CMake packages.
- `ament_python`: common build system for Python packages.
- `package.xml`: package metadata and dependency source of truth.
- `CMakeLists.txt`, `setup.py`, `setup.cfg`: package build, install, and entry-point configuration.
- `vcs` and `.repos`: common multi-repository checkout and import workflow.
- underlays and overlays: source `/opt/ros/<distro>/setup.*` first, then the workspace overlay.

## Runtime Introspection

- `ros2 node`: inspect nodes and graph participants.
- `ros2 topic`: list, echo, hz, bw, info, and publish topics.
- `ros2 service`: list, type, call, and inspect services.
- `ros2 action`: inspect and send action goals.
- `ros2 param`: list, get, set, dump, and load parameters.
- `ros2 interface`: inspect message, service, and action definitions.
- `ros2 doctor`: environment and graph health checks.
- `ros2 bag`: record, play, inspect, and reproduce runtime behavior.
- `rqt`: GUI inspection, graph, console, plot, and bag workflows when available.

## Robot Description And Frames

- URDF: robot model structure for links, joints, geometry, collision, and inertial properties.
- `xacro`: macro system commonly used to keep URDF maintainable.
- `tf2`: transform tree and frame lookup system.
- `robot_state_publisher`: publishes robot transforms from joint states and robot description.
- `joint_state_publisher` and `joint_state_publisher_gui`: publish or manually adjust joint states for development.
- RViz2 fixed frame, TF tree, model, marker, point cloud, laser scan, image, and path displays are common debugging surfaces.

## Launch And Configuration

- Python launch files are the most flexible default for non-trivial systems.
- XML and YAML launch files are valid when the repository already uses them or the launch is simple.
- Parameter YAML files are preferred for repeatable node configuration.
- Namespaces, remaps, launch arguments, substitutions, event handlers, and included launch files are common composition tools.
- Lifecycle nodes are common for managed startup, activation, deactivation, cleanup, and shutdown.
- Composable nodes are common when reducing process overhead or enabling intra-process communication.

## Simulation And Visualization

- RViz2: visualization and graph-level debugging.
- Gazebo / `ros_gz`: common physics simulation path for ROS 2 robots.
- Webots and other simulators may be repository-specific; use only when the project already depends on them or the user asks.
- `rosbag2`: reproducible runtime evidence for debugging, regression tests, and offline analysis.
- Simulator checks are safer defaults before hardware checks when the behavior can be reproduced there.

## Control, Navigation, And Manipulation

- `ros2_control`: common hardware abstraction and controller framework.
- `ros2_controllers`: common controllers for `ros2_control`.
- Nav2: common mobile robot navigation stack.
- MoveIt 2: common manipulation and motion planning stack.
- Treat these as adjacent stacks for the base `ros2-development` skill. Use them for integration and routing, but consider separate specialist skills for deep controller, navigation, manipulation, or robot-specific behavior.
- Confirm distro support before relying on these stacks, especially immediately after a new ROS 2 distribution release.

## CI, Lint, Test, And Release

- `colcon test` and `colcon test-result --all --verbose`: common test execution and result inspection.
- `ament_lint`, `ament_lint_auto`, and package-specific linters: common style and quality gates.
- `pytest`: common Python test runner.
- GTest/GMock: common C++ unit test stack.
- `launch_testing`: common integration test path for launch and graph behavior.
- `ros-tooling/setup-ros`: common GitHub Action for setting up ROS.
- `ros-tooling/action-ros-ci`: common GitHub Action for building and testing ROS 2 packages with `colcon`.
- Docker and devcontainers: common reproducible development and CI environments.
- `bloom`, rosdistro, and the ROS build farm: common release workflow for public ROS packages.

## Middleware, Networking, And Security

- DDS/RMW is a ROS 2 core concern; behavior can differ across middleware implementations.
- Fast DDS and Cyclone DDS are common RMW choices. Use the repository or distro default unless there is a concrete reason to change.
- `ROS_DOMAIN_ID` separates ROS graphs on the same network.
- QoS policies are central for sensors, commands, latched-style state, bag replay, lossy links, and reliable control paths.
- SROS2 and ROS 2 security tooling matter when networked robots, shared networks, or sensitive operations are in scope.

## Common Routing Boundaries

- Use this skill for ROS 2 workspace, package, graph, launch, debug, simulation, container, and CI work.
- Route deep Nav2 behavior to a navigation-focused skill if one exists.
- Route deep MoveIt 2 behavior to a manipulation-focused skill if one exists.
- Route deep `ros2_control` controller design to a controls-focused skill if one exists.
- Route micro-ROS firmware, RTOS, and microcontroller transport work to a dedicated embedded or micro-ROS workflow if one exists.
- Route mechanical CAD and circuit design to engineering design skills.

## Source Pointers

- ROS documentation: https://docs.ros.org/
- ROS 2 distributions: https://docs.ros.org/en/lyrical/Releases.html
- ROS 2 package index: https://index.ros.org/
- colcon tutorial: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- rosdep tutorial: https://docs.ros.org/en/rolling/Tutorials/Intermediate/Rosdep.html
- QoS concept guide: https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html
- Launch concept guide: https://docs.ros.org/en/rolling/Concepts/Basic/About-Launch.html
- ros-tooling/action-ros-ci: https://github.com/ros-tooling/action-ros-ci
