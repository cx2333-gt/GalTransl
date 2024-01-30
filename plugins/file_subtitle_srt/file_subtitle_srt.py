import json,re
from GalTransl import LOGGER
from GalTransl.GTPlugin import GFilePlugin


class text_common_normalfix(GFilePlugin):

    def gtp_init(self, plugin_conf: dict, project_conf: dict):
        """
        This method is called when the plugin is loaded.
        在插件加载时被调用。
        plugin_conf为插件yaml中Settings下的设置。
        project_conf为项目yaml中common下的设置。
        :param plugin_conf: The settings for the plugin.
        :param project_conf: The settings for the project.
        """
        self.pattern = re.compile(r'(\d+)\n([\d:,]+ --> [\d:,]+)\n(.+?)(?=\n\d+|\Z)', re.DOTALL)
        

    def load_file(self, file_path: str)->list:
        """
        This method is called to load a file.
        加载文件时被调用。
        :param file_path: The path of the file to load.
        :return: A list of CSentense objects.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            srt_text = file.read()
        
        try:
            matches = self.pattern.findall(srt_text)
            result = [{"index": int(m[0]), "timestamp": m[1], "message": m[2].strip()} for m in matches]
        except Exception as e:
            LOGGER.error(f"Error parsing srt file: {e}")
            raise e

        return result

    def save_file(self, file_path: str, result_json: list):
        """
        This method is called to save a file.
        保存文件时被调用。
        :param file_path: The path of the file to save.
        :param sentenses: A list of CSentense objects to save.
        """

        result = ""
        for item in result_json:
            result += f"{item['index']}\n{item['timestamp']}\n{item['message']}\n\n"

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(result.strip())


    
    def gtp_final(self):
        """
        This method is called after all translations are done.
        在所有文件翻译完成之后的动作，例如输出提示信息。
        """
        pass