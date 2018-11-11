# coding=utf-8
from tensor2tensor.utils import registry
from tensor2tensor.data_generators import problem, text_problems

@registry.register_problem
class MyProblem(text_problems.Text2ClassProblem):

    vec_path = ''

    @property
    def is_generate_per_split(self):
        return True

    @property
    def dataset_splits(self):
        return [{
            "split": problem.DatasetSplit.TRAIN,
            "shards": 5,
        }, {
            "split": problem.DatasetSplit.EVAL,
            "shards": 1,
        }]

    @property
    def approx_vocab_size(self):
        return 2 ** 10  # 8k vocab suffices for this small dataset.

    @property
    def num_classes(self):
        return 2

    @property
    def vocab_filename(self):
        return "my_problem.vocab.%d" % self.approx_vocab_size

    def generate_samples(self, data_dir, tmp_dir, dataset_split):
        del data_dir
        del tmp_dir
        del dataset_split

        with open(self.vec_path) as input_feature:
            label = 1
            for line in input_feature:
                label += 1
                yield {
                    "inputs": line.strip(),
                    "label": label % 2
                }

#  t2t-trainer --t2t_usr_dir=. --data_dir=../train_data_feature --problem=my_problem --model=transformer --hparams_set=transformer_base --output_dir=../output_new
