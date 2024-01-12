import json
import config
import time




class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            # Your initialization code here
            cls._instance.file_name = f"../log/log_{time.time()}.txt"
        return cls._instance

    def record_metafile(self, path, imagename, scoring_types):
        meta_file = f'../images/{path}/metadata.jsonl'
        meta_data = {}
        meta_data['file_name'] = imagename
        meta_data['label'] = []
        for score_type in scoring_types:
            meta_data['label'].append(score_type -1 )
        # meta_data['label'] = [scoring_types[0] - 1, scoring_types[1] - 1, scoring_types[2] - 1,
        #                       scoring_types[3] - 1, scoring_types[4] - 1]
        with open(meta_file, 'a') as file:
            json.dump(meta_data, file)
            file.write('\n')

    def record_txtfile(self, imagepath, scoring_types):
        with open(self.file_name, 'a') as file:
            file.write(f"***********{imagepath}***************\n")
            for i, score_type in enumerate(scoring_types):
                file.write(f"{config.ID_PATTERN[i+1]}: {config.score_map[score_type]}\n")
            # file.write(f"big rectangle {score_map[scoring_types[0]]}\n")
            # file.write(f"big cross {score_map[scoring_types[1]]}\n")
            # file.write(f"horizontal middle line {score_map[scoring_types[2]]}\n")
            # file.write(f"vertical middle line {score_map[scoring_types[3]]}\n")
            # file.write(f"small rectangle with cross {score_map[scoring_types[4]]}\n")

    def record_detail(self, text):
        with open(self.file_name, 'a') as file:
            file.write(text)
            file.write('\n')
