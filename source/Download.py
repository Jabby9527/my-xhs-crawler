from pathlib import Path

from requests import exceptions
from requests import get

from .Manager import Manager

__all__ = ['Download']


class Download:
    manager = Manager()

    def __init__(
            self,
            root: Path,
            path: str,
            folder: str,
            headers: dict,
            proxies=None,
            chunk=1024 * 1024, ):
        self.temp = root.joinpath("./temp")
        self.root = self.__init_root(root, path, folder)
        self.headers = self.__delete_cookie(headers)
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.chunk = chunk

    def __init_root(self, root: Path, path: str, folder: str) -> Path:
        if path and (r := Path(path)).is_dir():
            root = r.joinpath(folder or "Download")
        else:
            root = root.joinpath(folder or "Download")
        root.mkdir(exist_ok=True)
        self.temp.mkdir(exist_ok=True)
        return root

    def run(self, urls: list, name: str, type_: int, log):
        if type_ == 0:
            self.__download(urls[0], f"{name}.mp4", log)
        elif type_ == 1:
            for index, url in enumerate(urls):
                self.__download(url, f"{name}_{index + 1}.jpeg", log)

    def __download(self, url: str, name: str, log):
        temp = self.temp.joinpath(name)
        file = self.root.joinpath(name)
        if self.manager.is_exists(file):
            self.output_prompt(f"文件 {name} 已存在，跳过下载！", log)
            return
        try:
            with get(url, headers=self.headers, proxies=self.proxies, stream=True) as response:
                with temp.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk):
                        f.write(chunk)
            self.manager.move(temp, file)
            self.output_prompt(f"文件 {name} 下载成功！", log)
        except exceptions.ChunkedEncodingError:
            self.manager.delete(temp)
            self.output_prompt(f"网络异常，文件 {name} 下载失败！", log)

    @staticmethod
    def __delete_cookie(headers: dict) -> dict:
        download_headers = headers.copy()
        del download_headers["Cookie"]
        return download_headers

    @staticmethod
    def output_prompt(tip: str, log):
        if log:
            log.write_line(tip)
        else:
            print(tip)
