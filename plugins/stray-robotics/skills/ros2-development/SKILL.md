---
name: "ros2-development"
description: "Use when the user wants to create, modify, debug, test, containerize, or CI-enable ROS 2 workspaces, packages, nodes, launch files, interfaces, simulations, or robot application integrations. Do not use for ROS 1-only projects, generic full-stack apps, pure mechanical CAD, pure circuit design, Nav2/MoveIt 2/ros2_control deep specialization, micro-ROS firmware work, or unsafe live robot operation without explicit hardware context and safety constraints."
---

# ROS 2 Development

Build and debug ROS 2 software systematically from workspace shape through graph design, implementation, build, test, simulation, packaging, and handoff. Treat live hardware as a separate safety boundary, not as an ordinary local runtime.

## Do Not Use For

- ROS 1-only projects, `catkin`, `roscore`, or `roslaunch` workflows except when identifying migration boundaries.
- Generic web, mobile, desktop, backend, or full-stack app work without a ROS 2 robotics workflow.
- Pure mechanical CAD, pure circuit design, enclosure design, or PCB work.
- Deep Nav2, MoveIt 2, `ros2_control`, micro-ROS, firmware, perception model training, or robot-specific stack ownership unless the user asks only for integration boundaries.
- Running commands that can move real hardware, enable actuators, start controllers, or connect to a networked robot before safety context and explicit approval are established.

## Decision Gates

1. Confirm the task is ROS 2, not ROS 1. If the repository mixes both, identify which packages and commands are ROS 2-owned before editing.
2. Identify the ROS 2 distribution, OS, install method, container or host runtime, target hardware or simulator, language, package type, and whether the work may affect real hardware.
3. Check current official ROS 2 distribution status before recommending a distro. As of June 1, 2026, Lyrical Luth is the latest ROS 2 LTS release, Jazzy Jalisco and Humble Hawksbill are still supported LTS releases, Kilted Kaiju is a supported non-LTS release, and Rolling Ridley is the development distribution.
4. Stop for confirmation before any live robot, actuator, controller, motor, safety-critical network, or destructive system-install command.
5. Route elsewhere when the real task is mechanical design, circuit design, general app work, product research, or a specialized robotics stack that deserves its own skill.

## Reference Loading

Load only the smallest reference needed for the task:

- `references/de-facto-tooling.md`: common ROS 2 tooling, adjacent stacks, CI, lint, release, simulation, visualization, and middleware choices when selecting an implementation or validation path.

## Workflow

1. Map the workspace before changing it.
   - Inspect `src/`, `package.xml`, `CMakeLists.txt`, `setup.py`, `setup.cfg`, `launch/`, `config/`, `test/`, `resource/`, `msg/`, `srv/`, `action/`, `urdf/`, `rviz/`, and CI or container files.
   - Identify underlays, overlays, generated interfaces, package dependencies, launch entry points, simulator assumptions, and install rules.
   - Source only the intended ROS 2 setup files for inspection commands, and avoid modifying `/opt/ros` or system package state unless explicitly requested.

2. Design the ROS graph explicitly.
   - Name nodes, components, topics, services, actions, parameters, namespaces, remaps, frames, lifecycle states, and launch composition.
   - Decide QoS policies intentionally for sensor data, commands, latched-style state, lossy streams, reliable control paths, and bag replay.
   - Account for DDS/domain IDs, executors, callback groups, composition, parameters, tf2 frames, and interface compatibility when they affect behavior.

3. Manage dependencies and package metadata.
   - Keep `package.xml` as the dependency source of truth and align it with `CMakeLists.txt`, `setup.py`, entry points, generated interfaces, and test dependencies.
   - Prefer `rosdep install --from-paths src --ignore-src -r -y` for dependency resolution in a workspace or container.
   - Use `ament_cmake` and `ament_python` conventions instead of ROS 1 `catkin` assumptions.

4. Implement the smallest coherent ROS 2 slice.
   - Update nodes, launch files, parameters, interfaces, config, install rules, tests, and docs together when the behavior spans them.
   - Keep generated interface changes compatible with downstream packages or clearly call out rebuild and migration requirements.
   - For hardware-adjacent work, provide simulator, dry-run, disabled-controller, or read-only inspection paths where feasible.

5. Build, source, and test with ROS 2 tooling.
   - Use `colcon build --symlink-install` by default for development builds unless repository guidance says otherwise.
   - Source the resulting overlay intentionally before running ROS 2 CLI or launch checks.
   - Run targeted tests with `colcon test`, then inspect failures with `colcon test-result --all --verbose`.
   - For Python packages, include lint, import, entry-point, and launch-related checks when available.

6. Debug from evidence in the ROS graph.
   - Use `ros2 doctor`, `ros2 node`, `ros2 topic`, `ros2 service`, `ros2 action`, `ros2 param`, `ros2 interface`, `ros2 launch`, `ros2 run`, and `ros2 bag` commands as appropriate.
   - Inspect message types, rates, QoS compatibility, parameters, lifecycle transitions, frames, logs, and bag replay behavior before guessing.
   - For launch issues, check substitutions, parameters, remaps, composable nodes, environment variables, and package install locations.

7. Validate simulation, visualization, containers, and CI where relevant.
   - Prefer isolated simulator or visualization verification before hardware verification.
   - Use `references/de-facto-tooling.md` when choosing between common ROS 2 tooling or adjacent stacks such as `ros2_control`, Nav2, MoveIt 2, Gazebo, RViz, lint, CI, release, or middleware options.
   - Use RViz, Gazebo, rosbag, and launch files to reproduce graph behavior when the repository supports them.
   - For reproducible environments, use official ROS container images, devcontainers, or repository-defined Dockerfiles.
   - For CI, prefer ROS-aware workflows such as `ros-tooling/action-ros-ci` when they match the repository.

8. Hand off with operational clarity.
   - Report the ROS 2 distro, workspace path, packages changed, graph behavior changed, commands run, and what was not verified.
   - Separate build/test/simulation evidence from hardware evidence.
   - Call out any required user-side sourcing, device permissions, domain ID, network, simulator asset, or hardware safety setup.

## Validation Expectations

- `rosdep install --from-paths src --ignore-src -r -y` or a clear explanation when dependency resolution is not run.
- `colcon build --symlink-install` or the repository's documented build command.
- `colcon test` and `colcon test-result --all --verbose` for changed packages when tests exist.
- Targeted ROS 2 CLI inspection for graph, interface, parameter, QoS, or launch changes.
- Simulator, RViz, Gazebo, or rosbag verification when the change depends on runtime graph behavior and the assets are available.
- Explicit "hardware not verified" wording unless live robot verification was requested, approved, and performed under stated constraints.

## Guardrails

- Do not run commands that can move a robot, enable actuators, start controllers, write to motor topics, or connect to production robot networks without explicit approval and safety context.
- Do not treat Rolling as a stable release. Verify release and support status from official ROS documentation when distro choice matters.
- Do not use EOL distribution docs as the primary source for a current implementation.
- Do not mix ROS 1 commands or package conventions into ROS 2 work unless the task is migration analysis.
- Do not hide system-level changes such as apt installs, udev rules, group membership, device permissions, DDS vendor changes, or environment variable requirements.
- Do not leave package metadata, install rules, launch files, generated interfaces, or tests stale after changing nodes.

## Reference URLs

- ROS documentation: https://docs.ros.org/
- ROS 2 distributions: https://docs.ros.org/en/lyrical/Releases.html
- colcon workspace tutorial: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- Creating a ROS 2 package: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html
- rosdep tutorial: https://docs.ros.org/en/rolling/Tutorials/Intermediate/Rosdep.html
- ROS 2 QoS: https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html
- Lifecycle node design: https://design.ros2.org/articles/node_lifecycle.html
- ROS 2 CI action: https://github.com/ros-tooling/action-ros-ci
- Docker ROS 2 guide: https://docs.docker.com/guides/ros2/develop/
- Local de facto tooling reference: `references/de-facto-tooling.md`

## Output Expectations

- Working ROS 2 code/config changes or a concrete blocker report.
- The selected ROS 2 distribution and whether it is LTS, supported non-LTS, or Rolling.
- A short graph-level summary: changed nodes, topics, services, actions, parameters, frames, QoS, launch files, and package boundaries.
- Build, test, dependency, launch, simulation, container, and CI evidence that was run or explicitly skipped.
- Hardware safety status and any commands the user must approve before live operation.
