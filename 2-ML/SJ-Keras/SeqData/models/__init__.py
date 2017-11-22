from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import models.model_ak4
import models.ak4_elu_gru
import models.ak4_elu

__all__ = ["model_ak4"]

def build_a_model(model_name, *args, **kargs):
    return getattr(models, model_name).build_a_graph(*args, **kargs)
