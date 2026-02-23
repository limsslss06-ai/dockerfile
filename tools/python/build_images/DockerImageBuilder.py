import os
import subprocess


class DockerImageBuilder:

    def __init__(
        self,
        search_path,
        search_mode="selected",  # "all" / "first" / "latest"/ "selected"
        root_path=None,
        build_context=None,
        build_args=None,
    ):

        self.search_path = search_path
        self.search_mode = search_mode
        self.root_path = root_path or os.path.dirname(search_path)
        self.build_context = build_context or os.path.dirname(search_path)
        self.build_args = build_args or {}

    def build(self, print_output=True):
        """build docker images"""
        dockerfiles = self.__get_all_Dockerfile_under_search_path()

        for df in dockerfiles:
            # cmd
            # cmd = ["docker", "build", "-f", df, "-t", image_name, self.build_context]
            # -f: 指定 Dockerfile 文件路径 | full path of the Dockerfile
            image_name = self.__default_naming(df)
            cmd = [
                "docker",
                "build",
                "-f",
                df,
                "-t",
                image_name,
                self.build_context,
            ]
            if self.build_args:
                for k, v in self.build_args.items():
                    cmd.extend(["--build-arg", f"{k}={v}"])
            if print_output:
                print(" ".join(cmd))

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error building Dockerfile ({df}): {result.stderr}")
            else:
                print(f"Successfully built Dockerfile ({df})")

    def __get_all_Dockerfile_under_search_path(self):
        """
        return type
        """
        dockerfiles = []

        for root, dirs, files in os.walk(self.search_path):  # recursive get files
            for f in files:
                if f.startswith("Dockerfile"):  # filter with "^Dockerfile"
                    dockerfiles.append(os.path.join(root, f))
        return dockerfiles

    def __default_naming(self, dockerfile_path):
        """
        <repository>:<tag>

        默认命名规则：
        repository =
           从 root_path 开始的 path_name, 去掉 Dockerfile 前缀
        tag = latest
        """

        # calculate relative path from root_path to dockerfile_path
        relative_path = os.path.relpath(dockerfile_path, self.root_path)

        # For example: service/api/Dockerfile.dev

        # separate dir part and file part
        dir_part = os.path.dirname(relative_path)  # service/api
        file_part = os.path.basename(relative_path)  # Dockerfile.dev

        if file_part == "Dockerfile":
            suffix = ""
        else:
            suffix = file_part.replace("Dockerfile", "").strip(".")

        # final repository
        if suffix:
            repository = f"{dir_part}/{suffix}" if dir_part else suffix
        else:
            repository = dir_part if dir_part else "image"

        repository = repository.replace("\\", "/").lower()

        tag = "latest"

        return f"{repository}:{tag}"
