from pyrsistent import CheckedPVector

from datapype.conf import FromConf, require, field


class PipelineStep(FromConf):
    def run_step(self, *args, **kwargs):
        raise NotImplementedError


class Pipeline(CheckedPVector):
    __type__ = PipelineStep

    def run(self):
        for step in self:
            step.run_step()


class FeatureList(CheckedPVector):
    __type__ = str


class TrainModelStep(PipelineStep):
    features = field(FeatureList)

    def run_step(self):
        raise NotImplementedError


@require(model_type='lr')
class TrainLRStep(TrainModelStep):
    def run_step(self):
        print('LR Model  {}'.format(self.features))


@require(model_type='gbt')
class TrainGBTStep(TrainModelStep):
    def run_step(self):
        print('GBT Model {}'.format(self.features))


pipeline = Pipeline([
    TrainModelStep.from_conf(
        model_type='lr',
        features=['a', 'b'],
    ),
    TrainModelStep.from_conf(
        model_type='gbt',
        features=['c', 'd'],
    ),
])


if __name__ == '__main__':
    print(pipeline)
    pipeline.run()
    print(pipeline == Pipeline.create(pipeline.serialize()))
