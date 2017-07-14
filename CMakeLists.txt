cmake_minimum_required(VERSION 2.8.3)
project(beginner_tutorials)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs genmsg geometry_msgs wire_msgs)

## Declare ROS messages and services
add_message_files(FILES Num.msg Num2.msg Person.msg Time.msg)
add_service_files(FILES AddTwoInts.srv AddTwoInts2.srv AddTwoInts3.srv Geometry_msgs_to_world_evidence.srv)

## Generate added messages and services
generate_messages(DEPENDENCIES std_msgs geometry_msgs wire_msgs )

## Declare a catkin package
catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs geometry_msgs wire_msgs
)

## Build talker and listener
add_executable(talker src/talker.cpp)
target_link_libraries(talker ${catkin_LIBRARIES})

add_executable(listener src/listener.cpp)
target_link_libraries(listener ${catkin_LIBRARIES})

## Build service client and server
include_directories(include ${catkin_INCLUDE_DIRS})
add_executable(add_two_ints_server src/add_two_ints_server.cpp)
target_link_libraries(add_two_ints_server ${catkin_LIBRARIES})
add_dependencies(add_two_ints_server beginner_tutorials_gencpp)

add_executable(add_two_ints_client src/add_two_ints_client.cpp)
target_link_libraries(add_two_ints_client ${catkin_LIBRARIES})
add_dependencies(add_two_ints_client beginner_tutorials_gencpp)

add_executable(basic_shapes src/basic_shapes.cpp)
target_link_libraries(basic_shapes ${catkin_LIBRARIES})
