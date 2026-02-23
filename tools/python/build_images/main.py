import os
import subprocess

from DockerImageBuilder import DockerImageBuilder


docker_dir = "../../../docker"

builder = DockerImageBuilder(
    search_path=docker_dir,
    search_mode="all",  # 构建所有 Dockerfile
    root_path= "../../..",  # root 用来生成 repository 名称
    build_context=docker_dir,
    build_args={"PYTHON_VERSION": "3.11"},  # 可选 build-arg
)

builder.build(print_output=True)